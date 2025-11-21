import random
import time
from dataclasses import dataclass

from textual import on
from textual.app import ComposeResult
from textual.message import Message
from textual.screen import Screen
from textual.validation import Number
from textual.widget import Widget
from textual.widgets import Button, Footer, Input

from mmath.config import CONFIG
from mmath.questions.operations import AnswerData, QuestionData, times_tables
from mmath.questions.question_screen import EndScreen
from mmath.questions.question_widgets import (
    AnswerBox,
    QuestionDisplay,
    QuestionNumber,
    QuestionUI,
)


@dataclass
class TimesTableConfig:
    times_table: int
    top: int
    number_of_questions: int


class ConfigureTimesTablesScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Input(
            type="integer",
            placeholder="Which times table?",
            validators=[
                Number(),
            ],
            id="times_table",
        )
        yield Input(
            type="integer",
            placeholder="Up to what number?",
            validators=[Number()],
            id="tt_top",
        )
        yield Input(
            type="integer",
            placeholder="How many questions?",
            validators=[Number()],
            id="tt_number_of_questions",
        )
        self.start_button = Button("Start", id="start_times_tables")
        self.back_button = Button("Back", classes="back_button")
        yield self.back_button
        yield self.start_button

    def on_input_changed(self) -> None:
        all_inputs = self.query(Input)
        self.start_button.disabled = not all(i.is_valid for i in all_inputs)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_times_tables":
            times_table = int(self.query_one("#times_table", Input).value)
            top = int(self.query_one("#tt_top", Input).value)
            number_of_questions = int(
                self.query_one("#tt_number_of_questions", Input).value
            )
            tt_config = TimesTableConfig(times_table, top, number_of_questions)
            self.app.push_screen(TimesTableScreen(tt_config))
        elif "back_button" in event.button.classes:
            self.dismiss()


class TimesTablesUI(Widget):
    def __init__(self, config: TimesTableConfig) -> None:
        super().__init__()
        self.config = config
        self.answer_data: dict[int, AnswerData] = {}

    def compose(self) -> ComposeResult:
        self.question_number = QuestionNumber()
        self.question_display = QuestionDisplay()
        self.answer_box = AnswerBox()
        yield self.question_number
        yield self.question_display
        yield self.answer_box

    def on_mount(self) -> None:
        self.new_question()

    class Finished(Message): ...

    def check_finished(self) -> None:
        if self.question_number.current == self.config.number_of_questions:
            self.post_message(self.Finished())

    def new_question(self) -> None:
        self.question_number.next()
        self.n_err = 0
        self.q_data = times_tables(self.config.top, self.config.times_table)
        self.question_display.update(self.q_data.display)
        self.time = time.time()

    @on(Input.Submitted)
    @on(Button.Pressed)
    def check_submission(self) -> None:
        submission = self.answer_box.answer_box.value
        if not submission:
            self.answer_box.answer_box.clear()
            return
        if int(self.answer_box.answer_box.value) == self.q_data.correct:
            self.answer_box.answer_box.clear()
            self.time = time.time() - self.time
            qdata = self.q_data
            answerdata = AnswerData(
                qdata.name, qdata.left, qdata.right, self.time, self.n_err
            )
            self.answer_data[self.question_number.current] = answerdata
            self.check_finished()
            self.new_question()
        else:
            self.n_err += 1


class TimesTableScreen(Screen):
    BINDINGS = CONFIG.DEFAULT_BINDINGS

    def __init__(self, config: TimesTableConfig) -> None:
        super().__init__()
        self.tt_config = config

    CSS_PATH = "questionui.tcss"

    def compose(self) -> ComposeResult:
        self.qui = TimesTablesUI(self.tt_config)
        yield self.qui
        yield Footer()

    async def on_times_tables_ui_finished(self) -> None:
        selected = await self.app.push_screen_wait(EndScreen(self.qui.answer_data))
        if selected == "yes_repeat":
            self.qui.question_number.current = 0
            self.qui.new_question()
        else:
            self.app.pop_screen()
