from typing import TYPE_CHECKING

from mmath.operations import (
    Addition,
    CelsiusToFahrenheit,
    ComplexMultiplication,
    FahrenheitToCelsius,
    FractionAddition,
    FractionMultiplication,
    KilogramsToPounds,
    KilometersToMiles,
    MilesToKilometers,
    Mod,
    Multiplication,
    PoundsToKilograms,
    QuestionInfo,
    Square,
    SquareRoot,
    Subtraction,
    TimesTables,
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
