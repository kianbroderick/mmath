from textual.app import App, ComposeResult
from textual.containers import (
    Center,
    Grid,
    Horizontal,
    HorizontalGroup,
    Right,
    VerticalScroll,
)
from textual.screen import Screen
from textual.validation import Number
from textual.widget import Widget
from textual.widgets import Button, Footer, Input, Label

from mmath.config import CONFIG


class InputMaxes(Widget):
    def __init__(self, selected_operations: list[str]) -> None:
        self.selected_operations = selected_operations
        self.operation_maxes: dict[str, int] = {}
        super().__init__()

    def compose(self) -> ComposeResult:
        for operation in self.selected_operations:
            with Horizontal(classes="input_maxes_class"):
                yield Label(operation.capitalize())
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
        with VerticalScroll(id="maxes_screen_container"):
            yield InputMaxes(self.selected_operations)
            yield Horizontal(
                self.back_button, self.submit_button, id="horizontal_input_maxes"
            )
        yield Footer()

    def on_input_changed(self) -> None:
        all_inputs = self.query(Input)
        self.submit_button.disabled = not all(i.value for i in all_inputs)

    def on_input_submitted(self) -> None:
        if self.submit_button.disabled:
            return
        else:
            for operation in self.selected_operations:
                input_value = self.query_one(f"#{operation}", Input)
                value = input_value.value
                self.input_maxes.operation_maxes[operation] = int(value)
            self.dismiss(self.input_maxes.operation_maxes)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if "back_button" in event.button.classes:
            self.app.pop_screen()
        if event.button.id == "submit_maxes":
            for operation in self.selected_operations:
                input_value = self.query_one(f"#{operation}", Input)
                value = input_value.value
                self.input_maxes.operation_maxes[operation] = int(value)
            self.dismiss(self.input_maxes.operation_maxes)

    def action_go_back(self) -> None:
        self.app.pop_screen()


class MainMenuTestApp(App):
    def compose(self) -> ComposeResult:
        yield InputMaxes(list(CONFIG.QUESTIONDATA.keys()))


if __name__ == "__main__":
    app = MainMenuTestApp()
    app.run()
