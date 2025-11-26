from typing import TYPE_CHECKING

from mmath.operations import (
    Addition,
    ComplexMultiplication,
    FractionAddition,
    FractionMultiplication,
    Mod,
    Multiplication,
    QuestionInfo,
    Square,
    SquareRoot,
    Subtraction,
    conversions,
    default,
    times_tables,
)

if TYPE_CHECKING:
    from textual.binding import BindingType


class Config:
    def __init__(self) -> None:
        self.QUESTIONDATA: dict[str, QuestionInfo] = {
            "addition": Addition,
            "subtraction": Subtraction,
            "multiplication": Multiplication,
            "square": Square,
            "square_root": SquareRoot,
            "mod": Mod,
            "complex_multiplication": ComplexMultiplication,
            "fraction_addition": FractionAddition,
            "fraction_multiplication": FractionMultiplication,
        }
        self.SPECIAL = {
            "times_tables": times_tables,
            "default": default,
            "conversions": conversions,
        }
        self.DEFAULT_BINDINGS: list[BindingType] = [
            ("q", "quit", "Quit"),
            ("d", "toggle_dark", "Toggle dark mode"),
        ]


CONFIG = Config()
