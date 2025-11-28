import random
import time
from dataclasses import dataclass

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal
from textual.message import Message
from textual.screen import ModalScreen, Screen
from textual.validation import Number
from textual.widget import Widget
from textual.widgets import Button, Footer, Input, Label, Switch

from mmath.config import CONFIG
from mmath.data.data_screen import EndScreen
from mmath.operations import AnswerData, QuestionData, times_tables
from mmath.questions.question_screen import QuestionScreen
from mmath.questions.question_widgets import (
    AnswerBox,
    QuestionDisplay,
    QuestionNumber,
    QuestionUI,
    in_bounds,
)


class ConfigurePowersScreen(ModalScreen):
    CSS_PATH = "../styles/config_times_table_screen.tcss"
    BINDINGS = [("b", "go_back", "Back")]

    def compose(self) -> ComposeResult:
        with Container(id="config_tt_main_container"):
            yield Label("Which base number?")
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
            yield Label("Up to what exponent?")
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
            self.timer_input = Input(
                type="number",
                id="timer_input",
                placeholder="Enter a number",
                validators=[Number(minimum=0.0001)],
                validate_on=("changed",),
            )
            self.timer_input.visible = False
            yield Horizontal(
                Label("Timer"),
                Switch(animate=False),
                self.timer_input,
                id="timer_container",
            )
            self.start_button = Button(
                "Start", id="start_times_tables", disabled=True, classes="next_button"
            )
            self.back_button = Button("Back", classes="back_button")
            yield Horizontal(self.back_button, Container(), self.start_button)
        yield Footer()

    def on_input_changed(self) -> None:
        self.check_ready()
        self.timer = self.timer_input.value

    def on_switch_changed(self) -> None:
        switch = self.query_one(Switch)
        if switch.value:
            self.timer_input.visible = True
        else:
            self.timer_input.visible = False
        self.check_ready()

    def check_ready(self) -> None:
        all_inputs = self.query(Input)
        switch = self.query_one(Switch)
        if switch.value:
            self.start_button.disabled = not all(
                i.value and i.is_valid for i in all_inputs
            )
        else:
            self.start_button.disabled = not all(
                i.value and i.is_valid for i in all_inputs if i.id != "timer_input"
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
        base_num = int(self.query_one("#times_table", Input).value)
        top = int(self.query_one("#tt_top", Input).value)
        number_of_questions = int(
            self.query_one("#tt_number_of_questions", Input).value
        )
        self.app.push_screen(
            QuestionScreen(
                {"powers": top},
                number_of_questions,
                self.timer,
                special=base_num,
            )
        )
