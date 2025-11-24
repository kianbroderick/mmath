import random
from dataclasses import dataclass
from math import floor, sqrt

DIVISOR_MAX: int = 5
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
    number_of_errors: int


def addition(top: int) -> QuestionData:
    name = "+"
    left = random.randint(1, top)
    right = random.randint(1, top)
    correct = (left + right, left + right)
    display = f"{left} + {right}"
    return QuestionData(name, left, right, correct, display)


def subtraction(top: int) -> QuestionData:
    name = "-"
    left = random.randint(1, top)
    right = random.randint(1, top)
    correct = (left - right, left - right)
    display = f"{left} - {right}"
    return QuestionData(name, left, right, correct, display)


def multiplication(top: int) -> QuestionData:
    name = "*"
    left = random.randint(1, top)
    right = random.randint(1, top)
    correct = (left * right, left * right)
    display = f"{left} * {right}"
    return QuestionData(name, left, right, correct, display)


def square(top: int) -> QuestionData:
    name = "^"
    left = random.randint(1, top)
    right = 2
    correct = (left**2, left**2)
    display = f"{left}^2"
    return QuestionData(name, left, right, correct, display)


def squareroot(top: int) -> QuestionData:
    name = "sqrt"
    left = random.randint(1, top)
    right = None
    true_root = sqrt(left)
    rounded = round(true_root)
    best_answer = rounded - (rounded**2 - left) / (2 * rounded)
    tol = best_answer * TOLERANCE
    correct = (
        min(true_root - tol, best_answer - tol),
        max(true_root + tol, best_answer + tol),
    )
    display = f"sqrt( {left} ){correct}"
    return QuestionData(name, left, right, correct, display)


def mod(top: int) -> QuestionData:
    name = "mod"
    left = random.randint(1, top)
    right = random.randint(1, max(floor(left / DIVISOR_MAX), 1))
    correct = (left % right, left % right)
    display = f"{left} mod {right}"
    return QuestionData(name, left, right, correct, display)


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
