from textual.app import App, ComposeResult
from textual.containers import (
    Center,
    Container,
    Grid,
    Horizontal,
    HorizontalGroup,
    Right,
    Vertical,
    VerticalScroll,
)
from textual.screen import Screen
from textual.validation import Number
from textual.widget import Widget
from textual.widgets import Button, Footer, Input, Label, Static, Switch

from mmath.config import CONFIG
from mmath.operations import display_text


class InputMaxes(Vertical):
    def __init__(self, selected_operations: list[str]) -> None:
        self.selected_operations = selected_operations
        self.operation_maxes: dict[str, int] = {}
        super().__init__()

    def compose(self) -> ComposeResult:
        for operation in self.selected_operations:
            with Horizontal(classes="input_maxes_class"):
                yield Label(display_text(operation))
                yield Input(
                    type="integer",
                    placeholder="Enter the maximum desired value",
                    classes="input_maxes",
                    id=operation,
                    validators=[Number(minimum=1)],
                    valid_empty=False,
                    validate_on=("changed",),
                )


class InputMaxesScreen(Screen):
    CSS_PATH = "../styles/maxes_screen.tcss"
    BINDINGS = [("b", "go_back", "Back")]

    def __init__(self, selected_operations: list[str]) -> None:
        self.selected_operations = selected_operations
        self.timer = None
        super().__init__()

    def compose(self) -> ComposeResult:
        self.input_maxes = InputMaxes(self.selected_operations)
        self.submit_button = Button(
            "Submit",
            classes="submit next_button",
            disabled=True,
            id="submit_maxes",
        )
        self.back_button = Button(
            "Back",
            classes="back_button",
        )
        self.timer_input = Input(
            type="number",
            id="timer_input",
            placeholder="Enter a number",
            validators=[Number(minimum=0.0001)],
            validate_on=("changed",),
        )
        self.timer_input.visible = False
        with VerticalScroll(id="maxes_screen_container"):
            yield InputMaxes(self.selected_operations)
            yield Horizontal(
                Label("Timer"),
                Switch(animate=False),
                self.timer_input,
                id="timer_container",
            )
            yield Horizontal(
                self.back_button,
                Container(),
                self.submit_button,
                id="horizontal_input_maxes",
            )
        yield Footer()

    def on_input_changed(self) -> None:
        self.check_ready()
        self.timer = self.timer_input.value

    def check_ready(self) -> None:
        all_inputs = self.query(Input)
        switch = self.query_one(Switch)
        if switch.value:
            self.submit_button.disabled = not all(
                i.value and i.is_valid for i in all_inputs
            )
        else:
            self.submit_button.disabled = not all(
                i.value and i.is_valid for i in all_inputs if i.id != "timer_input"
            )

    def on_switch_changed(self) -> None:
        switch = self.query_one(Switch)
        if switch.value:
            self.timer_input.visible = True
        else:
            self.timer_input.visible = False
        self.check_ready()

    def on_input_submitted(self) -> None:
        if self.submit_button.disabled:
            return
        else:
            self.return_data()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if "back_button" in event.button.classes:
            self.app.pop_screen()
        if event.button.id == "submit_maxes":
            self.return_data()

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def return_data(self) -> None:
        for operation in self.selected_operations:
            input_value = self.query_one(f"#{operation}", Input)
            value = input_value.value
            self.input_maxes.operation_maxes[operation] = int(value)
        self.dismiss((self.input_maxes.operation_maxes, self.timer))


class MainMenuTestApp(App):
    def compose(self) -> ComposeResult:
        yield InputMaxes(list(CONFIG.QUESTIONDATA.keys()))


if __name__ == "__main__":
    app = MainMenuTestApp()
    app.run()
