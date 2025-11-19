import operator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from textual.binding import BindingType


class Config:
    def __init__(self) -> None:
        self.OPERATIONS: dict[str, Callable[[int, int], int]] = {
            "addition": operator.add,
            "subtraction": operator.sub,
            "multiplication": operator.mul,
        }
        self.SYMBOLS: dict[str, str] = {
            "addition": "+",
            "subtraction": "-",
            "multiplication": "*",
        }
        self.DEFAULT_BINDINGS: list[BindingType] = [
            ("q", "quit", "Quit"),
            ("d", "toggle_dark", "Toggle dark mode"),
        ]


CONFIG = Config()
