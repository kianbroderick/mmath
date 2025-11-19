from dataclasses import dataclass
from typing import TYPE_CHECKING

from textual import on
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer

if TYPE_CHECKING:
    from textual.app import ComposeResult


@dataclass
class QuestionData:
    operation: str
    left: int
    right: int
    time: float
    number_of_errors: int


class DataScreen(Screen):
    def __init__(self, data: dict[int, QuestionData]) -> None:
        super().__init__()
        self.data = data

    def compose(self) -> ComposeResult:
        self.sort_time_button = Button()
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
