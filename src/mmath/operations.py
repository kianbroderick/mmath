import random
from dataclasses import dataclass


@dataclass
class QuestionData:
    name: str
    left: float
    right: float | None
    correct: float
    display: str


@dataclass
class AnswerData:
    operation: str
    left: float
    right: float | None
    time: float
    number_of_errors: int


def addition(top: int) -> QuestionData:
    name = "addition"
    left = random.randint(1, top)
    right = random.randint(1, top)
    correct = left + right
    display = f"{left} + {right}"
    return QuestionData(name, left, right, correct, display)


def subtraction(top: int) -> QuestionData:
    name = "subtraction"
    left = random.randint(1, top)
    right = random.randint(1, top)
    correct = left - right
    display = f"{left} - {right}"
    return QuestionData(name, left, right, correct, display)


def multiplication(top: int) -> QuestionData:
    name = "multiplication"
    left = random.randint(1, top)
    right = random.randint(1, top)
    correct = left * right
    display = f"{left} * {right}"
    return QuestionData(name, left, right, correct, display)


def times_tables(top: int, num: int) -> QuestionData:
    name = "times tables"
    other_num = random.randint(1, top)
    if random.random() < 0.5:
        left, right = (num, other_num)
    else:
        left, right = (other_num, num)
    correct = left * right
    display = f"{left} * {right}"
    return QuestionData(name, left, right, correct, display)
