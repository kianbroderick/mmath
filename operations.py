import datetime
import random
import time
from collections.abc import Callable
from dataclasses import dataclass
from math import ceil, floor, gcd, sqrt
from typing import Any

from colorama import Fore

from utils import (
    enter_to_cont,
    get_day,
    get_expr,
    get_float,
    get_int,
    in_bounds,
)

##################################################################################################
# These should all be functions that take a single input,
# the maximum number you are asked to compute.
# They should input a single random question to the screen, time how long it
# takes to answer that question correctly, and track how many mistakes.
# They should all return a QuestionResult object.
# Special cases can be given a specific config function in config.py
#
# Be sure to add new functions to the ALL_OPERATIONS dictionary in config.py
##################################################################################################


###########################################################
# defines how close a guess has to be for a correct answer
# a value of 0.01 means that an answer has to be within 1%
# of the right answer to be correct
TOLERANCE: float = 0.01

# rounding num for the printed range in conv
ROUND_NUM: int = 6


@dataclass
class QuestionResult:
    num_wrong: int
    question_time: float
    question_info: tuple[str, str, str] | tuple[str, str]


correct = f"{Fore.GREEN}--   correct --{Fore.RESET}"


def wrong() -> int:
    print(f"{Fore.RED}--   wrong   --\n{Fore.RESET}")
    return 1


def print_ticket(ticket: dict[str, Any], *, units: str = "") -> None:
    msg_width: int = max(map(len, ticket.keys()))
    num_width: int = max(len(f"{x:.{ROUND_NUM}f}") for x in ticket.values())
    print()
    for msg, num in ticket.items():
        print(
            f"{Fore.BLUE}{msg:<{msg_width}}"
            f"{Fore.YELLOW}{num:>{num_width}.{ROUND_NUM}f}"
            f"{Fore.BLUE} {units}{Fore.RESET}"
        )
    enter_to_cont()


def addition(top: int) -> QuestionResult:
    num_wrong: int = 0
    a: int = random.randint(1, top)
    b: int = random.randint(1, top)
    start: float = time.time()
    ans: int = get_int(f"{a} + {b} = ")
    while ans != (a + b):
        num_wrong += wrong()
        ans = get_int(f"{a} + {b} = ")
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, ("+", str(a), str(b)))


def subtraction(top: int) -> QuestionResult:
    num_wrong: int = 0
    a: int = random.randint(1, top)
    b: int = random.randint(1, top)
    start: float = time.time()
    ans: int = get_int(f"{a} - {b} = ")
    while ans != (a - b):
        num_wrong += wrong()
        ans = get_int(f"{a} - {b} = ")
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, ("-", str(a), str(b)))


def plus_minus(top: int) -> QuestionResult:
    if random.random() < 0.5:  # noqa: PLR2004
        return addition(top)
    return subtraction(top)


def multiplication(top: int) -> QuestionResult:
    num_wrong: int = 0
    a: int = random.randint(1, top)
    b: int = random.randint(1, top)
    start: float = time.time()
    ans: int = get_int(f"{a} * {b} = ")
    while ans != (a * b):
        num_wrong += wrong()
        ans = get_int(f"{a} * {b} = ")
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, ("*", str(a), str(b)))


def times_tables(top: int, num: int) -> QuestionResult:
    num_wrong: int = 0
    other_num: int = random.randint(1, top)
    if random.random() < 0.5:  # noqa: PLR2004
        a: int = num
        b: int = other_num
    else:
        a = other_num
        b = num
    start: float = time.time()
    ans: int = get_int(f"{a} * {b} = ", pos=True)
    while ans != (a * b):
        num_wrong += wrong()
        ans = get_int(f"{a} * {b} = ", pos=True)
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, ("*", str(num), str(other_num)))


def powers(top: int, base: int) -> QuestionResult:
    num_wrong: int = 0
    exponent: int = random.randint(1, top)
    start: float = time.time()
    ans: int = get_int(f"{base}^{exponent} = ", pos=True)
    while ans != (base**exponent):
        num_wrong += wrong()
        ans = get_int(f"{base}^{exponent} = ", pos=True)
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, ("^", str(base), str(exponent)))


# Defines what the maximum divisor will be.
# A value of 5 makes the largest possible divisor
# one-fifth of the dividend.
DIVISOR_MAX: int = 5


def division(top: int) -> QuestionResult:
    num_wrong: int = 0
    dividend: int = random.randint(1, top)
    divisor: int = random.randint(1, max(floor(dividend / DIVISOR_MAX), 1))
    print(f"{dividend} / {divisor} = ")
    start: float = time.time()
    quotient: int = get_int("Quotient = ")
    remainder: int = get_int("Remainder = ")
    while (quotient, remainder) != divmod(dividend, divisor):
        num_wrong += wrong()
        print(f"{dividend} / {divisor} = ")
        quotient = get_int("Quotient = ")
        remainder = get_int("Remainder = ")
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, ("/", str(dividend), str(divisor)))


def modular(top: int) -> QuestionResult:
    num_wrong: int = 0
    a: int = random.randint(1, top)
    m: int = random.randint(1, max(floor(a / DIVISOR_MAX), 1))
    start: float = time.time()
    ans = get_int(f"{a} mod {m} = ")
    while ans != a % m:
        num_wrong += wrong()
        ans = get_int(f"{a} mod {m} = ")
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, ("mod", str(a), str(m)))


def square(top: int) -> QuestionResult:
    num_wrong: int = 0
    a: int = random.randint(1, top)
    start: float = time.time()
    ans: int = get_int(f"{a}^2 = ")
    while int(ans) != (a**2):
        num_wrong += wrong()
        ans = get_int(f"{a}^2 = ")
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, ("^", str(a), "2"))


def squareroot(top: int) -> QuestionResult:
    num_wrong: int = 0
    a: int = random.randint(1, top)
    true_root: float = sqrt(a)
    rounded: int = round(true_root)
    best_answer: float = rounded - (rounded**2 - a) / (2 * rounded)
    tol = best_answer * TOLERANCE
    correct_range = (
        min(true_root - tol, best_answer - tol),
        max(true_root + tol, best_answer + tol),
    )
    start: float = time.time()
    ans: float = get_expr(f"sqrt({a}) = ")
    while not in_bounds(ans, correct_range[0], correct_range[1], include=True):
        num_wrong += wrong()
        ans = get_expr(f"sqrt({a}) = ")
    q_time: float = time.time() - start
    ticket: dict[str, float | tuple] = {
        "Newton's method approximation: ": best_answer,
        "Actual: ": true_root,
        "Difference: ": best_answer - true_root,
        # "Accepted Range: ": correct_range,
    }
    print_ticket(ticket)
    return QuestionResult(num_wrong, q_time, ("sqrt", str(a)))


def perfect_square(top: int) -> QuestionResult:
    num_wrong: int = 0
    top = floor(sqrt(top))
    a: int = random.randint(1, top)
    start: float = time.time()
    ans: float = get_int(f"sqrt({a**2}) = ")
    while ans != a:
        num_wrong += wrong()
        ans = get_expr(f"sqrt({a**2}) = ")
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, ("sqrt", str(a**2)))


def print_complex_number(a: int, b: int) -> str:
    if b > 0:
        return f"{a} + {b}i"
    return f"{a} - {abs(b)}i"


def complex_multiplication(top: int) -> QuestionResult:
    num_wrong: int = 0
    a: int = random.randint(-1 * top, top)
    b: int = random.randint(-1 * top, top)
    c: int = random.randint(-1 * top, top)
    d: int = random.randint(-1 * top, top)
    print(f"({print_complex_number(a, b)}) * ({print_complex_number(c, d)}) = ")
    start: float = time.time()
    real_part_ans: int = get_int("Real = ")
    imaj_part_ans: int = get_int("Imaj = ")
    while (real_part_ans, imaj_part_ans) != (a * c - b * d, a * d + b * c):
        num_wrong += wrong()
        print(f"({print_complex_number(a, b)}) * ({print_complex_number(c, d)}) = ")
        real_part_ans = get_int("Real = ")
        imaj_part_ans = get_int("Imaj = ")
    q_time: float = time.time() - start
    return QuestionResult(
        num_wrong,
        q_time,
        ("*", f"({print_complex_number(a, b)})", f"({print_complex_number(c, d)})"),
    )


def default() -> Callable[[], QuestionResult]:
    ops: list[tuple[Callable[[int], QuestionResult], int]] = [
        (addition, 999),
        (subtraction, 999),
        (multiplication, 99),
        (division, 999),
        (square, 99),
        (squareroot, 99),
    ]

    def inner() -> QuestionResult:
        func, limit = random.choice(ops)
        return func(limit)

    return inner


def random_date() -> datetime.date:
    start = datetime.date(1600, 1, 1)
    end = datetime.date(2099, 12, 31)
    return datetime.date.fromordinal(random.randint(start.toordinal(), end.toordinal()))


def calendar() -> QuestionResult:
    num_wrong: int = 0
    a = random_date()
    start: float = time.time()
    ans: int = get_day(f"The day of the week of {a.strftime('%B %d, %Y')} is ")
    while ans != ((a.weekday() + 1) % 7):
        num_wrong += wrong()
        ans = get_day(f"The day of the week of {a.strftime('%B %d, %Y')} is ")
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, ("cal", a.strftime("%B %d, %Y")))


def distance_conv(top: int) -> QuestionResult:
    if random.random() < 0.5:
        orig: str = "miles"
        orig_short: str = "mi"
        to: str = "kilometers"
        to_short: str = "km"
        ratio: float = 1.609344
        approx: float = 1.6
    else:
        orig = "kilometers"
        orig_short = "km"
        to = "miles"
        to_short = "mi"
        ratio = 0.621371
        approx = 0.625
    num_wrong: int = 0
    a = random.randint(1, top)
    start: float = time.time()
    correct: float = ratio * a
    closest_integer: int = round(correct)
    tol = TOLERANCE * correct
    lower_bound: int = floor(min([correct - tol, closest_integer, a * approx]))
    upper_bound: int = ceil(max([correct + tol, closest_integer, a * approx]))
    print(f"{a} {orig}")
    ans: float = get_float(f"{to.capitalize()}: ")
    while not in_bounds(ans, lower_bound, upper_bound, include=True):
        num_wrong += wrong()
        print(f"{a} {orig}")
        ans = get_float(f"{to.capitalize()}: ")
    q_time: float = time.time() - start
    ticket: dict[str, float | str] = {
        "Exact: ": ratio * a,
        "You were off by ": abs(ans - correct),
        "1.6 approximation: ": a * approx,
        "Closest integer: ": closest_integer,
        # "Accepted range: ": f"{(lower_bound, upper_bound)}",
    }
    print_ticket(ticket, units=to_short)
    return QuestionResult(num_wrong, q_time, (f"{orig_short} -> {to_short}", f"{a}"))


def temp_conv(top: int) -> QuestionResult:
    if random.random() < 0.5:  # noqa: PLR2004
        orig: str = "Fahrenheit"
        orig_short: str = "F"
        to: str = "Celsius"
        to_short: str = "C"
        conversion = lambda x: (x - 32) * (5 / 9)
        approx = lambda x: (x - 30) / 2
    else:
        orig = "Celsius"
        orig_short = "C"
        to = "Fahrenheit"
        to_short = "F"
        conversion = lambda x: x * 1.8 + 32
        approx = lambda x: x * 2 + 30
    num_wrong: int = 0
    a = random.randint(1, top)
    start: float = time.time()
    correct: float = conversion(a)
    tol: float = correct * TOLERANCE
    closest_integer: int = round(correct)
    print(f"{a}° {orig}")
    ans: float = get_float(f"{to.capitalize()}: ")
    lower_bound: int = floor(min(correct - tol, approx(a), closest_integer))
    upper_bound: int = ceil(max(correct + tol, approx(a), closest_integer))
    while not in_bounds(ans, lower_bound, upper_bound, include=True):
        num_wrong += wrong()
        print(f"{a}° {orig}")
        ans = get_float(f"{to.capitalize()}: ")
    q_time: float = time.time() - start
    ticket: dict[str, float] = {
        "Exact: ": conversion(a),
        "You were off by ": abs(ans - correct),
        "Approximation: ": approx(a),
        "Closest integer: ": closest_integer,
    }
    print_ticket(ticket, units=f"°{to_short}")
    return QuestionResult(num_wrong, q_time, (f"{orig_short} -> {to_short}", f"{a}"))


def pounds_kg(top: int) -> QuestionResult:
    num_wrong: int = 1
    if random.random() < 0.5:  # noqa: PLR2004
        orig: str = "pounds"
        orig_short: str = "lb"
        to: str = "kilograms"
        to_short: str = "kg"
        conversion = lambda x: x * 0.45359237
        approx = lambda x: x * 0.45
    else:
        orig = "kilograms"
        orig_short = "kg"
        to = "pounds"
        to_short = "lb"
        conversion = lambda x: x * 2.20462
        approx = lambda x: x * 2.2
    a = random.randint(1, top)
    start: float = time.time()
    correct: float = conversion(a)
    closest_integer: int = round(correct)
    tol = TOLERANCE * correct
    print(f"{a} {orig}")
    ans: float = get_float(f"{to.capitalize()}: ")
    lower_bound: int = floor(min(correct - tol, approx(a), closest_integer))
    upper_bound: int = ceil(max(correct + tol, approx(a), closest_integer))
    while not in_bounds(ans, lower_bound, upper_bound, include=True):
        num_wrong += wrong()
        print(f"{a} {orig}")
        ans = get_float(f"{to.capitalize()}: ")
    q_time: float = time.time() - start
    ticket: dict[str, float] = {
        "Exact: ": conversion(a),
        "You were off by ": abs(ans - correct),
        "Approximation: ": approx(a),
        "Closest integer: ": closest_integer,
    }
    print_ticket(ticket, units=to_short)
    return QuestionResult(num_wrong, q_time, (f"{orig_short} -> {to_short}", f"{a}"))


def conversions(top: int) -> QuestionResult:
    trial = random.choice([temp_conv, pounds_kg, distance_conv])
    return trial(top)


def tip(top: int) -> QuestionResult:
    num_wrong: int = 0
    bill: float = round(random.randint(0, top * 100) / 100, 2)
    tips: list[int] = [5, 10, 15, 20, 25]
    tip = round(random.choice(tips), 2)
    tip_amount: float = (tip / 100) * bill
    start: float = time.time()
    print(f"{tip}% tip on ${bill:.2f} is")
    tip_amount_ans: float = get_float("Tip:   $")
    # checks if the answer is within +- 3 cents of the correct answer,
    # to account for rounding differences
    while not in_bounds(
        tip_amount_ans, tip_amount - 0.03, tip_amount + 0.03, include=True
    ):
        num_wrong += wrong()
        print(f"{tip}% tip on ${bill:.2f} is")
        tip_amount_ans = get_float("Tip:   $")
    print(correct)
    total_ans: float = get_float("Total: $")
    total_amount: float = bill + tip_amount_ans
    while not in_bounds(
        total_ans, total_amount - 0.03, total_amount + 0.03, include=True
    ):
        num_wrong += wrong()
        print(f"{tip}% tip on ${bill:.2f} is")
        print(f"Tip:   ${tip_amount_ans}")
        total_ans = get_float("Total: $")
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, ("%", str(tip), str(bill)))


def simplify_fraction(num: int, denom: int) -> tuple[int, int]:
    common_factor = gcd(num, denom)
    if common_factor == 0:
        return (0, 0)
    return (num // common_factor, denom // common_factor)


def frac_add(top: int) -> QuestionResult:
    num_wrong: int = 0
    a: int = random.randint(1, top)
    b: int = random.randint(1, top)
    c: int = random.randint(1, top)
    d: int = random.randint(1, top)
    if random.random() < 0.5:  # noqa: PLR2004
        op: str = "+"
        correct_num, correct_denom = simplify_fraction(a * d + b * c, b * d)
    else:
        op = "-"
        correct_num, correct_denom = simplify_fraction(a * d - b * c, b * d)
    start: float = time.time()
    print(f"{a}/{b} + {c}/{d}")
    num_ans: int = get_int("Numerator: ")
    denom_ans: int = get_int("Denominator: ")
    while num_ans != correct_num and denom_ans != correct_denom:
        num_wrong += wrong()
        num_ans = get_int("Numerator: ")
        denom_ans = get_int("Denominator: ")
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, (op, f"{a}/{b}", f"{c}/{d}"))


def frac_mult(top: int) -> QuestionResult:
    num_wrong: int = 0
    a: int = random.randint(1, top)
    b: int = random.randint(1, top)
    c: int = random.randint(1, top)
    d: int = random.randint(1, top)
    correct_num, correct_denom = simplify_fraction(a * c, b * d)
    start: float = time.time()
    print(f"{a}/{b} * {c}/{d}")
    num_ans: int = get_int("Numerator: ")
    denom_ans: int = get_int("Denominator: ")
    while num_ans != correct_num and denom_ans != correct_denom:
        num_wrong += wrong()
        num_ans = get_int("Numerator: ")
        denom_ans = get_int("Denominator: ")
    q_time: float = time.time() - start
    return QuestionResult(num_wrong, q_time, ("*", f"{a}/{b}", f"{c}/{d}"))


def fraction_all(top: int) -> QuestionResult:
    if random.random() < 0.5:  # noqa: PLR2004
        return frac_add(top)
    return frac_mult(top)
