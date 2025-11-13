import random
import statistics
from collections.abc import Callable

from colorama import Fore

from operations import (
    QuestionResult,
    addition,
    calendar,
    complex_multiplication,
    conversions,
    default,
    distance_conv,
    division,
    frac_add,
    frac_mult,
    fraction_all,
    modular,
    multiplication,
    perfect_square,
    plus_minus,
    pounds_kg,
    powers,
    square,
    squareroot,
    subtraction,
    temp_conv,
    times_tables,
    tip,
)
from utils import get_int, get_maxes, get_str

ROUNDING_NUM: int = 2


# Used to list options, be sure to see ALL_OPERATIONS at the bottom of this file
ALL_OPTIONS: dict[tuple[str, ...], str] = {
    ("+",): "addition",
    ("-",): "subtraction",
    ("+/-", "pm", "+-"): "addition and subtraction",
    ("f+",): "fraction addition",
    ("f*",): "fraction multiplication",
    ("frac",): "fraction addition and multiplication",
    ("*",): "multiplication",
    ("complex",): "complex multiplication",
    ("/",): "division with remainder",
    ("mod",): "mod function",
    ("^2", "sq"): "square",
    ("pow",): "powers of a specified base",
    ("sqrt",): "square root",
    ("psq",): "identify perfect squares",
    ("times tables", "tt"): "times tables",
    ("cal",): "find day of the week",
    ("dist",): "convert between miles and km",
    ("temp",): "convert between Fahrenheit and Celsius",
    ("weight",): "convert between pounds and kilograms",
    ("conv",): "all conversions",
    ("tip",): "calculate tips on a bill",
    ("custom",): "configure custom session",
    ("default",): "3 digit addition/subtraction, 2 digit multiplication, "
    "3 digit division, 2 digit squaring/square root",
}


def print_options() -> None:
    width: int = max(len(", ".join(v)) for v in ALL_OPTIONS)
    for op, desc in ALL_OPTIONS.items():
        aliases: str = ", ".join(op)
        print(f"{Fore.YELLOW} {aliases:>{width}}" + f"{Fore.BLUE} | {desc}{Fore.RESET}")
    print("\n")


def configure() -> tuple[str, int]:
    operations: list[str] = [alias for key_tuple in ALL_OPTIONS for alias in key_tuple]
    while True:
        print(
            f"{Fore.BLUE}What do you want to practice? "
            f"Enter {Fore.YELLOW}l{Fore.BLUE} for options.{Fore.RESET}"
        )
        op: str = get_str(f"{Fore.GREEN}Operation: {Fore.RESET}").lower().strip()
        if op == "l":
            print_options()
            continue
        if op in operations:
            break
        print(f"{Fore.RED}Invalid input.{Fore.RESET}")
    print(f"{Fore.BLUE}How many questions?{Fore.RESET}")
    num_q: int = get_int(f"{Fore.GREEN}Enter a number: {Fore.RESET}", pos=True)
    return op, num_q


# These are the options that are included in the 'custom' setting
CUSTOM_OPERATIONS: dict[str, Callable[[int], QuestionResult]] = {
    "addition": addition,
    "subtraction": subtraction,
    "multiplication": multiplication,
    "complex multiplication": complex_multiplication,
    "division": division,
    "square": square,
    "square root": squareroot,
    "fraction addition": frac_add,
    "fraction multiplication": frac_mult,
    "distance conversion": distance_conv,
    "temperature conversion": temp_conv,
    "weight conversion": pounds_kg,
    "tip calculation": tip,
}


def configure_custom() -> Callable[[], QuestionResult]:
    while True:
        user_opts: dict[str, int] = {}
        for operation in CUSTOM_OPERATIONS:
            top = get_maxes(operation)
            if top:
                user_opts[operation] = top
        if not user_opts:
            print(f"{Fore.RED}Error: please specify at least one maximum.{Fore.RESET}")
            continue
        break

    def custom() -> QuestionResult:
        question = random.choice(list(user_opts.keys()))
        return CUSTOM_OPERATIONS[question](user_opts[question])

    return custom


def configure_times_tables() -> Callable[[int], QuestionResult]:
    print(f"{Fore.BLUE}Which times table do you want to practice?{Fore.RESET}")
    table_number: int = get_int(f"{Fore.GREEN}Enter a number: {Fore.RESET}", pos=True)

    def inner(top: int) -> QuestionResult:
        return times_tables(top, table_number)

    return inner


def configure_powers() -> Callable[[int], QuestionResult]:
    print(f"{Fore.BLUE}Which base number do you want to practice?{Fore.RESET}")
    base: int = get_int(f"{Fore.GREEN}Enter a number: {Fore.RESET}", pos=True)

    def inner(top: int) -> QuestionResult:
        return powers(top, base)

    return inner


def print_summary(
    num_q: int, errors: int, start_round: float, end_round: float, q_times: list[float]
) -> None:
    print(
        f"{Fore.BLUE}Solved "
        f"{Fore.YELLOW}{num_q}"
        f"{Fore.BLUE} problems in "
        f"{Fore.YELLOW}{end_round - start_round:.{ROUNDING_NUM}f}"
        f"{Fore.BLUE} seconds with "
        f"{Fore.YELLOW}{errors}"
        f"{Fore.BLUE} {'error' if errors == 1 else 'errors'}.\n{Fore.RESET}"
    )
    if len(q_times) > 1:
        stats: dict[str, float] = {
            "Average time:": statistics.mean(q_times),
            "Standard deviation:": statistics.stdev(q_times),
            "Median time:": statistics.median(q_times),
            "Shortest time:": min(q_times),
            "Longest time:": max(q_times),
            "Range:": max(q_times) - min(q_times),
        }
        l_width = max(map(len, stats.keys())) + 1  # + 1 so there is a space after
        num_width = max(len(f"{x:.{ROUNDING_NUM}f}") for x in stats.values())
        for desc, val in stats.items():
            print(
                f"{Fore.BLUE}{desc:<{l_width}}"
                f"{Fore.YELLOW}{val:>{num_width}.{ROUNDING_NUM}f}{Fore.BLUE} seconds{Fore.RESET}"
            )


ALL_OPERATIONS: dict[str, Callable[..., QuestionResult]] = {
    "+": addition,
    "-": subtraction,
    "+/-": plus_minus,
    "pm": plus_minus,
    "+-": plus_minus,
    "*": multiplication,
    "f+": frac_add,
    "f*": frac_mult,
    "frac": fraction_all,
    "complex": complex_multiplication,
    "/": division,
    "mod": modular,
    "^2": square,
    "sq": square,
    "pow": powers,
    "sqrt": squareroot,
    "psq": perfect_square,
    "times tables": times_tables,
    "tt": times_tables,
    "cal": calendar,
    "dist": distance_conv,
    "temp": temp_conv,
    "weight": pounds_kg,
    "conv": conversions,
    "tip": tip,
    "default": default(),
}
