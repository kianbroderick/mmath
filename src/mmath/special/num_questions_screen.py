from typing import TYPE_CHECKING

from textual import on
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label

if TYPE_CHECKING:
    from textual.app import ComposeResult


class NumberOfQuestionsScreen(ModalScreen):
    CSS_PATH = "../styles/number_of_questions_screen.tcss"
    BINDINGS = [("b,q", "back", "Back")]

    def compose(self) -> ComposeResult:
        with Container(id="num_questions_container"):
            yield Label("How many questions?")
            yield Input(placeholder="Enter a number", type="integer")
            with Horizontal():
                yield Button("Back", classes="back_button")
                yield Container()
                self.submit_button = Button(
                    "Submit", classes="next_button", disabled=True
                )
                yield self.submit_button

    def action_leave(self) -> None:
        submission = self.query_one(Input).value
        if not submission:
            return
        self.dismiss(int(submission))

    @on(Input.Submitted)
    def on_input_submitted(self) -> None:
        self.action_leave()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if "next_button" in event.button.classes:
            self.action_leave()
        if "back_button" in event.button.classes:
            self.action_back()

    @on(Input.Changed)
    def check_button(self, event: Input.Changed) -> None:
        submission = event.input.value
        if submission:
            self.submit_button.disabled = False
        else:
            self.submit_button.disabled = True

    def action_back(self) -> None:
        self.app.pop_screen()
