from typing import TYPE_CHECKING

from textual import events, on
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.validation import Number
from textual.widgets import Button, Input, Label, Switch

if TYPE_CHECKING:
    from textual.app import ComposeResult


class NumberOfQuestionsScreen(ModalScreen):
    CSS_PATH = "../styles/number_of_questions_screen.tcss"
    BINDINGS = [("escape", "back", "Back")]

    def compose(self) -> ComposeResult:
        with Container(id="num_questions_container"):
            yield Label("How many questions?")
            self.qnum = Input(placeholder="Enter a number", type="integer")
            yield self.qnum
            self.timer_input = Input(
                type="number",
                id="timer_input",
                placeholder="Enter a number",
                validators=[Number(minimum=0.0001)],
                validate_on=("changed",),
            )
            self.timer_input.visible = False
            self.vanish_input = Input(
                type="number",
                id="vanish_input",
                placeholder="Enter a number",
                validators=[Number(minimum=0.0001)],
                validate_on=("changed",),
            )
            self.vanish_input.visible = False
            yield Horizontal(
                Label("Timer"),
                Switch(animate=False, id="timer_switch"),
                self.timer_input,
                id="timer_container",
            )
            yield Horizontal(
                Label("Vanish"),
                Switch(animate=False, id="vanish_switch"),
                self.vanish_input,
                id="vanish_container",
            )
            with Horizontal():
                yield Button("Back", classes="back_button")
                yield Container()
                self.submit_button = Button(
                    "Submit", classes="next_button", disabled=True
                )
                yield self.submit_button

    def action_leave(self) -> None:
        if self.submit_button.disabled:
            return
        self.dismiss((int(self.qnum.value), self.timer_input.value, self.vanish))

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

    def check_ready(self) -> None:
        all_inputs = self.query(Input)
        timer_switch = self.query_one("#timer_switch", Switch)
        vanish_switch = self.query_one("#vanish_switch", Switch)
        if timer_switch.value and vanish_switch.value:
            self.submit_button.disabled = not all(
                i.value and i.is_valid for i in all_inputs
            )
        elif timer_switch.value:
            self.submit_button.disabled = not all(
                i.value and i.is_valid for i in all_inputs if i.id != "vanish_input"
            )
        elif vanish_switch.value:
            self.submit_button.disabled = not all(
                i.value and i.is_valid for i in all_inputs if i.id != "timer_input"
            )
        elif timer_switch.value and vanish_switch.value:
            self.submit_button.disabled = not all(
                i.value and i.is_valid for i in all_inputs
            )
        else:
            self.submit_button.disabled = not all(
                i.value and i.is_valid
                for i in all_inputs
                if i.id not in ["timer_input", "vanish_input"]
            )

    def on_input_changed(self) -> None:
        self.check_ready()
        self.timer = self.timer_input.value
        self.vanish = self.vanish_input.value

    def on_switch_changed(self, event=Switch.Changed) -> None:
        if event.switch.id == "timer_switch":
            self.timer_input.visible = event.switch.value
            self.timer_input.clear()
        elif event.switch.id == "vanish_switch":
            self.vanish_input.visible = event.switch.value
            self.vanish_input.clear()
        self.check_ready()

    def action_back(self) -> None:
        self.app.pop_screen()
