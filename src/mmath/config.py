from calendar import Calendar
from typing import TYPE_CHECKING

from mmath.operations import (
    Addition,
    Calendar,
    CelsiusToFahrenheit,
    ComplexMultiplication,
    Division,
    FahrenheitToCelsius,
    FractionAddition,
    FractionMultiplication,
    KilogramsToPounds,
    KilometersToMiles,
    MilesToKilometers,
    Mod,
    Multiplication,
    PerfectSquareRoot,
    PoundsToKilograms,
    Powers,
    QuestionInfo,
    Square,
    SquareRoot,
    Subtraction,
    TimesTables,
    default,
)

if TYPE_CHECKING:
    from textual.binding import BindingType


class Config:
    def __init__(self) -> None:
        self.QUESTIONDATA: dict[str, QuestionInfo] = {
            "addition": Addition,
            "subtraction": Subtraction,
            "multiplication": Multiplication,
            "division": Division,
            "square": Square,
            "square_root": SquareRoot,
            "perfect_square_root": PerfectSquareRoot,
            "mod": Mod,
            "complex_multiplication": ComplexMultiplication,
            "fraction_addition": FractionAddition,
            "fraction_multiplication": FractionMultiplication,
            "fahrenheit_to_celsius": FahrenheitToCelsius,
            "celsius_to_fahrenheit": CelsiusToFahrenheit,
            "kilometers_to_miles": KilometersToMiles,
            "miles_to_kilometers": MilesToKilometers,
            "pounds_to_kilograms": PoundsToKilograms,
            "kilograms_to_pounds": KilogramsToPounds,
        }
        self.ALLOPERATIONS: dict[str, QuestionInfo] = {
            "addition": Addition,
            "subtraction": Subtraction,
            "multiplication": Multiplication,
            "square": Square,
            "square_root": SquareRoot,
            "perfect_square_root": PerfectSquareRoot,
            "mod": Mod,
            "complex_multiplication": ComplexMultiplication,
            "fraction_addition": FractionAddition,
            "fraction_multiplication": FractionMultiplication,
            "fahrenheit_to_celsius": FahrenheitToCelsius,
            "celsius_to_fahrenheit": CelsiusToFahrenheit,
            "kilometers_to_miles": KilometersToMiles,
            "miles_to_kilometers": MilesToKilometers,
            "pounds_to_kilograms": PoundsToKilograms,
            "kilograms_to_pounds": KilogramsToPounds,
            "times_tables": TimesTables,
            "powers": Powers,
            "division": Division,
            "calendar": Calendar,
        }
        self.SPECIAL = {
            "times_tables": TimesTables,
            "default": default,
            "calendar": Calendar,
            "powers": Powers,
        }
        self.DEFAULT_BINDINGS: list[BindingType] = [
            ("q", "quit", "Quit"),
            ("d", "toggle_dark", "Toggle dark mode"),
        ]


CONFIG = Config()
