from statistics import mean, median, stdev
from typing import TYPE_CHECKING

from textual import on
from textual.containers import Grid
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, DataTable, Footer, Label

from mmath.config import CONFIG

if TYPE_CHECKING:
    from textual.app import ComposeResult

    from mmath.questions.operations import AnswerData


class DataScreen(Screen):
    def __init__(self, data: dict[int, AnswerData]) -> None:
        super().__init__()
        self.data = data

    def compose(self) -> ComposeResult:
        self.sort_time_button = Button("Sort by time")
        self.table = DataTable()
        self.exit_button = Button("Exit", id="exit_data_screen")
        yield self.sort_time_button
        yield self.table
        yield self.exit_button
        yield Footer()

    def on_mount(self) -> None:
        self.table.add_columns(
            "question", "operation", "left", "right", "time", "mistakes"
        )
        for question_number, data in self.data.items():
            self.table.add_row(
                question_number,
                data.operation,
                data.left,
                data.right,
                data.time,
                data.number_of_errors,
            )

    @on(Button.Pressed)
    def close_data_screen(self, event: Button.Pressed) -> None:
        if event.button.id == "exit_data_screen":
            self.app.pop_screen()


class EndScreen(ModalScreen):
    """Screen where you can get data, restart, or go back to mainmenu."""

    BINDINGS = CONFIG.DEFAULT_BINDINGS

    def __init__(self, data: dict[int, AnswerData]) -> None:
        super().__init__()
        self.data = data

    def compose(self) -> ComposeResult:
        self.summary_table = DataTable()
        yield self.summary_table
        yield Grid(
            Label("Repeat?", id="question"),
            Button("Data", id="view_data_button"),
            Button("No", variant="error", id="no_repeat"),
            Button("Yes", variant="primary", id="yes_repeat"),
            id="dialog",
        )
        yield Footer()

    def on_mount(self) -> None:
        times = [x.time for x in self.data.values()]
        average = mean(times)
        std_dev = stdev(times) if len(times) > 1 else 0
        data_median = median(times)
        minimum = min(times)
        maximum = max(times)
        data_range = maximum - minimum
        self.summary_table.add_columns(
            "average", "standard deviation", "median", "minimum", "maximum", "range"
        )
        self.summary_table.add_row(
            average, std_dev, data_median, minimum, maximum, data_range
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "view_data_button":
            self.app.push_screen(DataScreen(data=self.data))
        else:
            self.dismiss(event.button.id)
