import datetime
import random
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import ceil, floor, gcd, sqrt
from sys import displayhook
from typing import Any, Optional, Protocol


def in_bounds(test: float, bounds: tuple[float, float]) -> bool:
    lower, upper = bounds
    return test >= lower and test <= upper


class NotAComplexNumberError(Exception): ...


def complex_number_parser(cnum: str) -> tuple[int, int]:
    ex = r"^([+-]?)\s*(\d*)\s*([+-])\s*(\d*)\s*\*?\s*[iIjJ]"
    numbers = re.match(ex, cnum)
    if numbers:
        real = int(numbers.group(1) + numbers.group(2))
        imag = int(numbers.group(3) + numbers.group(4))
    else:
        raise NotAComplexNumberError
    return (real, imag)


def print_complex_number(a: int, b: int) -> str:
    if b > 0:
        return f"{a} + {b}i"
    return f"{a} - {abs(b)}i"


class NotAFractionError(Exception): ...


def simplify_fraction(num: int, denom: int) -> tuple[int, int]:
    common_factor = gcd(num, denom)
    if common_factor == 0:
        raise ZeroDivisionError
    return (num // common_factor, denom // common_factor)


def parse_fraction(fraction: str) -> tuple[int, int]:
    ex = r"([0-9]*)\s*/\s*([0-9]*)"
    numbers = re.match(ex, fraction)
    if numbers:
        num = int(numbers.group(1))
        denom = int(numbers.group(2))
    else:
        raise NotAFractionError
    return (num, denom)


def display_fraction(num: float | str, denom: float | str) -> str:
    return f"{num} / {denom}"


def parse_division(ans: str) -> tuple[int, int]:
    ex = r"(\d+)(?:\s*[rR]\s*(\d+))?"
    numbers = re.match(ex, ans)
    if numbers:
        quotient = int(numbers.group(1))
        remainder = int(numbers.group(2)) if numbers.group(2) else 0
    else:
        raise ValueError
    return (quotient, remainder)


def display_text(text: str) -> str:
    return text.replace("_", " ").title()


class QuestionInfo(ABC):
    textual_input_type: str | None = None
    input_restrictions: str | None = None

    def __init__(self, **kwargs: int) -> None:
        self.left: float | str = ""
        self.right: float | str = ""
        self.symbol: str = ""
        self.correct: float | complex | tuple[int, int] | None = None
        self.display: str = ""
        self.special: dict[str, int] | None = kwargs

    @abstractmethod
    def new(self, top: int) -> None:
        """Generate a new question."""

    @abstractmethod
    def verify_correct(self, usr_input: str) -> bool:
        """Check correctness."""


DIVISOR_MAX: int = 2
TOLERANCE: float = 0.01


@dataclass
class QuestionData:
    name: str
    left: float
    right: float | None
    correct: tuple[float, float]
    display: str


@dataclass
class AnswerData:
    operation: str
    left: float
    right: float | None
    time: float
    number_of_errors: int | str


def times_tables(top: int, num: int) -> QuestionData:
    name = "*"
    other_num = random.randint(1, top)
    if random.random() < 0.5:
        left, right = (num, other_num)
    else:
        left, right = (other_num, num)
    correct = (left * right, left * right)
    display = f"{left} * {right}"
    return QuestionData(name, left, right, correct, display)


class TimesTables(QuestionInfo):
    textual_input_type = "integer"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "×"
        num = self.special["num"]
        other_num = random.randint(1, top)
        if random.random() < 0.5:
            left, right = (num, other_num)
        else:
            left, right = (other_num, num)
        self.left = left
        self.right = right
        self.correct = self.left * self.right
        self.display = f"{self.left} × {self.right}"

    def verify_correct(self, usr_input: str) -> bool:
        try:
            return int(usr_input) == self.correct
        except ValueError:
            return False


class Powers(QuestionInfo):
    textual_input_type = "integer"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "^"
        self.left = self.special["num"]
        self.right = random.randint(1, top)
        self.correct = self.left**self.right
        self.display = f"{self.left}^{self.right}"

    def verify_correct(self, usr_input: str) -> bool:
        try:
            return int(usr_input) == self.correct
        except ValueError:
            return False


default = {
    "addition": 999,
    "subtraction": 999,
    "multiplication": 99,
    "square_root": 99,
    "square": 99,
}

conversions = {}


class Addition(QuestionInfo):
    textual_input_type = "integer"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "+"
        self.left = random.randint(1, top)
        self.right = random.randint(1, top)
        self.correct = self.left + self.right
        self.display = f"{self.left} + {self.right}"

    def verify_correct(self, usr_input: str) -> bool:
        try:
            return int(usr_input) == self.correct
        except ValueError:
            return False


class Subtraction(QuestionInfo):
    textual_input_type = "integer"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "-"
        self.left = random.randint(1, top)
        self.right = random.randint(1, self.left)
        self.correct = self.left - self.right
        self.display = f"{self.left} - {self.right}"

    def verify_correct(self, usr_input: str) -> bool:
        try:
            return int(usr_input) == self.correct
        except ValueError:
            return False


class Multiplication(QuestionInfo):
    textual_input_type = "integer"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "×"
        self.left = random.randint(1, top)
        self.right = random.randint(1, top)
        self.correct = self.left * self.right
        self.display = f"{self.left} × {self.right}"

    def verify_correct(self, usr_input: str) -> bool:
        try:
            return int(usr_input) == self.correct
        except ValueError:
            return False


class Division(QuestionInfo):
    textual_input_type = "text"
    input_restrictions = "[0123456789rR\\s]*"

    def new(self, top: int) -> None:
        self.symbol = "÷"
        self.left = random.randint(1, top)
        self.right = random.randint(1, max(floor(self.left / DIVISOR_MAX), 1))
        self.correct = divmod(self.left, self.right)
        self.display = f"{self.left} ÷ {self.right}"

    def verify_correct(self, usr_input: str) -> bool:
        correct_quotient, correct_remainder = self.correct
        try:
            usr_quotient, usr_remainder = parse_division(usr_input)
        except ValueError:
            return False
        return usr_quotient == correct_quotient and usr_remainder == correct_remainder


class Square(QuestionInfo):
    textual_input_type = "integer"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "^"
        self.left = random.randint(1, top)
        self.right = 2
        self.correct = self.left**2
        self.display = f"{self.left}^2"

    def verify_correct(self, usr_input: str) -> bool:
        try:
            return int(usr_input) == self.correct
        except ValueError:
            return False


class Mod(QuestionInfo):
    textual_input_type = "integer"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "mod"
        self.left = random.randint(1, top)
        self.right = random.randint(1, max(floor(self.left / DIVISOR_MAX), 1))
        self.correct = self.left % self.right
        self.display = f"{self.left} mod {self.right}"

    def verify_correct(self, usr_input: str) -> bool:
        try:
            return int(usr_input) == self.correct
        except ValueError:
            return False


class SquareRoot(QuestionInfo):
    textual_input_type = "number"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "sqrt"
        self.left = random.randint(1, top)
        self.display = f"√{self.left}"
        self.correct = sqrt(self.left)

    def verify_correct(self, usr_input: str) -> bool:
        try:
            rounded = round(self.correct)
            best_answer = rounded - (rounded**2 - self.left) / (2 * rounded)
            tol = best_answer * TOLERANCE
            correct_bounds = (
                floor(min(self.correct - tol, best_answer - tol)),
                ceil(max(self.correct + tol, best_answer + tol)),
            )
            return in_bounds(float(usr_input), correct_bounds)
        except ValueError, TypeError:
            return False


class ComplexMultiplication(QuestionInfo):
    textual_input_type = "text"
    input_restrictions = r"[\+\-\*\s0123456789iIjJ]*"

    def new(self, top: int) -> None:
        self.symbol = "*"
        a = random.randint(-top, top)
        b = random.randint(-top, top)
        c = random.randint(-top, top)
        d = random.randint(-top, top)
        first = complex(a, b)
        second = complex(c, d)
        self.left = print_complex_number(a, b)
        self.right = print_complex_number(c, d)
        self.correct = first * second
        self.display = (
            f"({print_complex_number(a, b)}) * ({print_complex_number(c, d)})"
        )

    def verify_correct(self, usr_input: str) -> bool:
        try:
            usr_real, usr_imag = complex_number_parser(usr_input)
            return usr_real == self.correct.real and usr_imag == self.correct.imag
        except ValueError, NotAComplexNumberError:
            return False


class FractionAddition(QuestionInfo):
    textual_input_type = "text"
    input_restrictions = r"[0123456789\/\s]*"

    def new(self, top: int) -> None:
        self.symbol = "+"
        a = random.randint(1, top)
        b = random.randint(1, top)
        c = random.randint(1, top)
        d = random.randint(1, top)
        a, b = simplify_fraction(a, b)
        c, d = simplify_fraction(c, d)
        self.left = display_fraction(a, b)
        self.right = display_fraction(c, d)
        self.correct = simplify_fraction(a * d + b * c, b * d)
        self.display = f"{display_fraction(a, b)} + {display_fraction(c, d)}"

    def verify_correct(self, usr_input: str) -> bool:
        correct_num, correct_denom = self.correct
        try:
            usr_num, usr_denom = parse_fraction(usr_input)
        except ValueError, NotAFractionError:
            return False
        return usr_num == correct_num and usr_denom == correct_denom


class FractionMultiplication(QuestionInfo):
    textual_input_type = "text"
    input_restrictions = r"[0123456789\/\s]*"

    def new(self, top: int) -> None:
        self.symbol = "*"
        a = random.randint(1, top)
        b = random.randint(1, top)
        c = random.randint(1, top)
        d = random.randint(1, top)
        a, b = simplify_fraction(a, b)
        c, d = simplify_fraction(c, d)
        self.left = display_fraction(a, b)
        self.right = display_fraction(c, d)
        self.correct = simplify_fraction(a * c, b * d)
        self.display = f"{display_fraction(a, b)} * {display_fraction(c, d)}"

    def verify_correct(self, usr_input: str) -> bool:
        correct_num, correct_denom = self.correct
        try:
            usr_num, usr_denom = parse_fraction(usr_input)
        except ValueError, NotAFractionError:
            return False
        return usr_num == correct_num and usr_denom == correct_denom


class CelsiusToFahrenheit(QuestionInfo):
    textual_input_type = "number"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "C -> F"
        self.left = random.randint(1, top)
        self.correct = self.left * 1.8 + 32
        self.display = f"{self.left}° Celsius to Fahrenheit"

    def verify_correct(self, usr_input: str) -> bool:
        approx = self.left * 2 + 30
        tol = self.correct * TOLERANCE
        lower_bound = floor(min(approx - tol, self.correct - tol))
        upper_bound = ceil(max(approx + tol, self.correct + tol))
        try:
            return in_bounds(float(usr_input), (lower_bound, upper_bound))
        except ValueError:
            return False


class FahrenheitToCelsius(QuestionInfo):
    textual_input_type = "number"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "F -> C"
        self.left = random.randint(1, top)
        self.correct = self.left - 32 / 1.8
        self.display = f"{self.left}° Celsius to Fahrenheit"

    def verify_correct(self, usr_input: str) -> bool:
        approx = (self.left - 30) / 2
        tol = self.correct * TOLERANCE
        lower_bound = floor(min(approx - tol, self.correct - tol))
        upper_bound = ceil(max(approx + tol, self.correct + tol))
        try:
            return in_bounds(float(usr_input), (lower_bound, upper_bound))
        except ValueError:
            return False


class PoundsToKilograms(QuestionInfo):
    textual_input_type = "number"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "lb -> kg"
        self.left = random.randint(1, top)
        self.correct = self.left * 0.45359237
        self.display = f"{self.left} pounds to kilograms"

    def verify_correct(self, usr_input: str) -> bool:
        approx = self.left * 0.45
        tol = self.correct * TOLERANCE
        lower_bound = floor(min(approx - tol, self.correct - tol))
        upper_bound = ceil(max(approx + tol, self.correct + tol))
        try:
            return in_bounds(float(usr_input), (lower_bound, upper_bound))
        except ValueError:
            return False


class KilogramsToPounds(QuestionInfo):
    textual_input_type = "number"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "kg -> lb"
        self.left = random.randint(1, top)
        self.correct = self.left * 2.20462
        self.display = f"{self.left} kilograms to pounds"

    def verify_correct(self, usr_input: str) -> bool:
        approx = self.left * 2.2
        tol = self.correct * TOLERANCE
        lower_bound = floor(min(approx - tol, self.correct - tol))
        upper_bound = ceil(max(approx + tol, self.correct + tol))
        try:
            return in_bounds(float(usr_input), (lower_bound, upper_bound))
        except ValueError:
            return False


class MilesToKilometers(QuestionInfo):
    textual_input_type = "number"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "mi -> km"
        self.left = random.randint(1, top)
        self.correct = self.left * 1.609344
        self.display = f"{self.left} miles to kilometers"

    def verify_correct(self, usr_input: str) -> bool:
        approx = self.left * 1.6
        tol = self.correct * TOLERANCE
        lower_bound = floor(min(approx - tol, self.correct - tol))
        upper_bound = ceil(max(approx + tol, self.correct + tol))
        try:
            return in_bounds(float(usr_input), (lower_bound, upper_bound))
        except ValueError:
            return False


class KilometersToMiles(QuestionInfo):
    textual_input_type = "number"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "km -> mi"
        self.left = random.randint(1, top)
        self.correct = self.left * 0.621371
        self.display = f"{self.left} kilometers to miles"

    def verify_correct(self, usr_input: str) -> bool:
        approx = self.left * 0.625
        tol = self.correct * TOLERANCE
        lower_bound = floor(min(approx - tol, self.correct - tol))
        upper_bound = ceil(max(approx + tol, self.correct + tol))
        try:
            return in_bounds(float(usr_input), (lower_bound, upper_bound))
        except ValueError:
            return False


def random_date() -> datetime.date:
    start = datetime.date(1600, 1, 1)
    end = datetime.date(2099, 12, 31)
    return datetime.date.fromordinal(random.randint(start.toordinal(), end.toordinal()))


class Calendar(QuestionInfo):
    textual_input_type = "text"
    input_restrictions = None

    def new(self, top: int) -> None:
        self.symbol = "cal"
        date_question = random_date()
        self.left = date_question.strftime("%B %d, %Y")
        self.correct = (date_question.weekday() + 1) % 7
        day = date_question.day
        self.display = (
            f"The day of the week of {date_question.strftime('%B {}, %Y').format(day)}"
        )

    def verify_correct(self, usr_input: str) -> bool:
        week_dict: dict[str, int] = {
            "sunday": 0,
            "sun": 0,
            "0": 0,
            "monday": 1,
            "mon": 1,
            "m": 1,
            "1": 1,
            "tuesday": 2,
            "tue": 2,
            "tues": 2,
            "t": 2,
            "2": 2,
            "wednesday": 3,
            "wed": 3,
            "w": 3,
            "3": 3,
            "thursday": 4,
            "thu": 4,
            "th": 4,
            "thurs": 4,
            "4": 4,
            "friday": 5,
            "fri": 5,
            "f": 5,
            "5": 5,
            "saturday": 6,
            "sat": 6,
            "6": 6,
        }
        return week_dict.get(usr_input.lower()) == self.correct
