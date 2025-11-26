import random
import time
from dataclasses import dataclass

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal
from textual.message import Message
from textual.screen import Screen
from textual.validation import Number
from textual.widget import Widget
from textual.widgets import Button, Footer, Input, Label

from mmath.config import CONFIG
from mmath.data.data_screen import EndScreen
from mmath.operations import AnswerData, QuestionData, times_tables
from mmath.questions.question_widgets import (
    AnswerBox,
    QuestionDisplay,
    QuestionNumber,
    QuestionUI,
    in_bounds,
)


@dataclass
class TimesTableConfig:
    times_table: int
    top: int
    number_of_questions: int


class ConfigureTimesTablesScreen(Screen):
    CSS_PATH = "../styles/config_times_table_screen.tcss"
    BINDINGS = [("b", "go_back", "Back")]

    def compose(self) -> ComposeResult:
        with Container(id="config_tt_main_container"):
            yield Label("Which times table?")
            yield Input(
                type="integer",
                placeholder="",
                validators=[
                    Number(minimum=1),
                ],
                validate_on=["changed"],
                valid_empty=False,
                id="times_table",
            )
            yield Label("Up to what number?")
            yield Input(
                type="integer",
                placeholder="",
                validators=[
                    Number(minimum=1),
                ],
                validate_on=["changed"],
                valid_empty=False,
                id="tt_top",
            )
            yield Label("How many questions?")
            yield Input(
                type="integer",
                placeholder="",
                validators=[
                    Number(minimum=1),
                ],
                validate_on=["changed"],
                valid_empty=False,
                id="tt_number_of_questions",
            )
            self.start_button = Button(
                "Start", id="start_times_tables", disabled=True, classes="next_button"
            )
            self.back_button = Button("Back", classes="back_button")
            yield Horizontal(self.back_button, Container(), self.start_button)
        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        all_inputs = self.query(Input)
        self.start_button.disabled = not all(
            (i.is_valid and bool(i.value)) for i in all_inputs
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if not self.start_button.disabled:
            self.action_start_quiz()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_times_tables":
            self.action_start_quiz()
        elif "back_button" in event.button.classes:
            self.dismiss()

    def action_go_back(self) -> None:
        self.dismiss()

    def action_start_quiz(self) -> None:
        times_table = int(self.query_one("#times_table", Input).value)
        top = int(self.query_one("#tt_top", Input).value)
        number_of_questions = int(
            self.query_one("#tt_number_of_questions", Input).value
        )
        tt_config = TimesTableConfig(times_table, top, number_of_questions)
        self.app.push_screen(TimesTableScreen(tt_config))


class TimesTablesUI(Widget):
    def __init__(self, config: TimesTableConfig) -> None:
        super().__init__()
        self.config = config
        self.answer_data: dict[int, AnswerData] = {}
        self.add_class("question-ui")

    def compose(self) -> ComposeResult:
        self.question_number = QuestionNumber()
        self.question_display = QuestionDisplay()
        self.answer_box = AnswerBox()
        yield self.question_number
        yield Center(self.question_display)
        yield self.answer_box

    def on_mount(self) -> None:
        self.new_question()

    class Finished(Message): ...

    def flash_class(self, widget, class_name: str, duration: float = 0.15) -> None:
        widget.add_class(class_name)
        self.set_timer(duration, lambda: widget.remove_class(class_name))

    def check_finished(self) -> bool:
        if self.question_number.current == self.config.number_of_questions:
            self.post_message(self.Finished())
            return True
        else:
            return False

    def new_question(self) -> None:
        if self.check_finished():
            return
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
        if in_bounds(float(self.answer_box.answer_box.value), self.q_data.correct):
            self.flash_class(self.answer_box.answer_box, "correct")
            self.flash_class(self.question_display, "correct")
            self.flash_class(self.question_number, "correct")
            self.flash_class(self, "correct")
            self.answer_box.answer_box.clear()
            self.time = time.time() - self.time
            qdata = self.q_data
            answerdata = AnswerData(
                qdata.name, qdata.left, qdata.right, self.time, self.n_err
            )
            self.answer_data[self.question_number.current] = answerdata
            self.new_question()
        else:
            self.answer_box.answer_box.clear()
            self.flash_class(self.answer_box.answer_box, "incorrect")
            self.flash_class(self.question_display, "incorrect")
            self.flash_class(self.question_number, "correct")
            self.flash_class(self, "incorrect")
            self.n_err += 1


class TimesTableScreen(Screen):
    BINDINGS = CONFIG.DEFAULT_BINDINGS

    def __init__(self, config: TimesTableConfig) -> None:
        super().__init__()
        self.tt_config = config

    CSS_PATH = "../styles/questionui.tcss"

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
