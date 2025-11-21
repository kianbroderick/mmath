from typing import TYPE_CHECKING

from mmath.questions.operations import (
    QuestionData,
    addition,
    multiplication,
    subtraction,
    times_tables,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from textual.binding import BindingType


class Config:
    def __init__(self) -> None:
        self.QUESTIONDATA: dict[str, Callable[[int], QuestionData]] = {
            "addition": addition,
            "subtraction": subtraction,
            "multiplication": multiplication,
        }
        self.SPECIAL = {"times_tables": times_tables}
        self.DEFAULT_BINDINGS: list[BindingType] = [
            ("q", "quit", "Quit"),
            ("d", "toggle_dark", "Toggle dark mode"),
        ]


CONFIG = Config()
