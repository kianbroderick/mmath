from statistics import mean, median, stdev
from typing import TYPE_CHECKING

from rich.text import Text
from textual import on
from textual.binding import BindingType
from textual.containers import Center, CenterMiddle, Container, Grid, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, DataTable, Footer, Label

from mmath.config import CONFIG

if TYPE_CHECKING:
    from textual.app import ComposeResult

    from mmath.operations import AnswerData


class DataScreen(Screen):
    CSS_PATH = "../styles/data_screen.tcss"
    BINDINGS = [
        ("d,b", "go_back", "Close"),
        ("q", "sort_by_q", "Sort by question"),
        ("t", "sort_by_time", "Sort by time"),
        ("o", "sort_by_op", "Sort by operation"),
        ("e", "sort_by_err", "Sort by errors"),
    ]

    def __init__(self, data: dict[int, AnswerData]) -> None:
        super().__init__()
        self.data = data

    def compose(self) -> ComposeResult:
        self.sort_qnum = Button("Sort by question", id="sort_q_btn", classes="sort_btn")
        self.sort_time = Button("Sort by time", id="sort_time_btn", classes="sort_btn")
        self.sort_op = Button("Sort by operation", id="sort_op_btn", classes="sort_btn")
        self.sort_err = Button("Sort by errors", id="sort_err_btn", classes="sort_btn")
        self.table = DataTable(zebra_stripes=True, cursor_type="none")
        self.exit_button = Button("Exit", id="exit_data_screen", classes="back_button")
        with VerticalScroll():
            with Grid(id="sorting_buttons"):
                yield self.sort_qnum
                yield self.sort_time
                yield self.sort_op
                yield self.sort_err
            yield Center(self.table)
            yield self.exit_button
        yield Footer()

    def on_mount(self) -> None:
        self.table.add_columns(
            ("question", "question"),
            ("left", "left"),
            ("op", "operation"),
            ("right", "right"),
            ("time", "time"),
            ("mistakes", "mistakes"),
        )
        for question_number, data in self.data.items():
            row = [
                question_number,
                data.left,
                data.operation,
                data.right,
                round(data.time, 2),
                data.number_of_errors,
            ]
            styled_row = [Text(str(cell), justify="right") for cell in row]
            self.table.add_row(*styled_row)

    @on(Button.Pressed)
    def close_data_screen(self, event: Button.Pressed) -> None:
        if event.button.id == "exit_data_screen":
            self.app.pop_screen()

    @on(Button.Pressed)
    def sort_table(self, event: Button.Pressed) -> None:
        if event.button.id == "sort_q_btn":
            self.action_sort_by_q()
        if event.button.id == "sort_time_btn":
            self.action_sort_by_time()
        if event.button.id == "sort_op_btn":
            self.action_sort_by_op()
        if event.button.id == "sort_err_btn":
            self.action_sort_by_err()

    def action_go_back(self) -> None:
        self.app.pop_screen()

    sort_time_reverse = False

    def action_sort_by_time(self) -> None:
        self.sort_time_reverse = not self.sort_time_reverse
        self.table.sort("time", reverse=self.sort_time_reverse)

    def action_sort_by_op(self) -> None:
        self.table.sort("operation", reverse=False)

    sort_q_reverse = False

    def action_sort_by_q(self) -> None:
        self.sort_q_reverse = not self.sort_q_reverse
        self.table.sort("question", reverse=self.sort_q_reverse)

    sort_err_reverse = False

    def action_sort_by_err(self) -> None:
        self.sort_err_reverse = not self.sort_err_reverse
        self.table.sort("mistakes", reverse=self.sort_err_reverse)


class EndScreen(ModalScreen):
    """Screen where you can get data, restart, or go back to mainmenu."""

    BINDINGS: list[BindingType] = [
        ("d", "goto_data_screen", "Data"),
        ("b", "mainmenu", "Exit to main menu"),
        ("r", "repeat", "Repeat"),
    ]
    CSS_PATH = "../styles/endscreen.tcss"

    def action_mainmenu(self) -> None:
        self.dismiss("")

    def __init__(self, data: dict[int, AnswerData]) -> None:
        super().__init__()
        self.data = data

    def compose(self) -> ComposeResult:
        total_time = sum([a.time for a in self.data.values()])
        number_of_questions = len(self.data)
        self.summary_table = DataTable(id="summary_data")
        yield Grid(
            Label(
                f"Completed {number_of_questions} questions in {total_time:.2f} seconds. Again?",
                id="question",
            ),
            Container(Center(self.summary_table), id="summary_data_container"),
            Button("Data", variant="default", id="view_data_button"),
            Button("Exit to menu", variant="error", id="no_repeat"),
            Button("Repeat", variant="success", id="yes_repeat"),
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
            "average", "std dev", "median", "minimum", "maximum", "range"
        )
        row = [average, std_dev, data_median, minimum, maximum, data_range]
        styled_row = [Text(f"{cell:.2f}", justify="right") for cell in row]
        self.summary_table.add_row(*styled_row)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "view_data_button":
            self.action_goto_data_screen()
        else:
            self.dismiss(event.button.id)

    def action_goto_data_screen(self) -> None:
        self.app.push_screen(DataScreen(data=self.data))

    def action_repeat(self) -> None:
        self.dismiss("yes_repeat")
