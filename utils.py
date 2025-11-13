import ast
import operator
import os
from collections.abc import Callable
from typing import Any

from colorama import Fore


class RestartProgram(Exception):
    pass


def clear_console() -> None:
    try:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    except Exception:
        print("\033c", end="")


def print_ui() -> None:
    clear_console()
    quit_text = f"{Fore.CYAN}Enter {Fore.YELLOW}q{Fore.CYAN} to quit  {Fore.RESET}"
    restart_text = (
        f"{Fore.CYAN}Enter {Fore.YELLOW}r{Fore.CYAN} to restart  {Fore.RESET}"
    )
    print(f"{quit_text}")
    print(f"{restart_text}")
    print("\n")


def quit_check(check: str) -> None:
    check = check.lower().strip()
    if check == "q":
        clear_console()
        raise SystemExit
    if check == "r":
        raise RestartProgram


def get_str(message: str = "") -> str:
    user_input = input(message).lower().strip()
    quit_check(user_input)
    return user_input


def get_maxes(operation: str) -> int | None:
    while True:
        user_input = (
            input(
                f"{Fore.BLUE}Enter a maximum for "
                f"{Fore.YELLOW}{operation.strip().lower()}"
                f"{Fore.BLUE}, or "
                f"{Fore.YELLOW}[Enter]"
                f"{Fore.BLUE} to skip: {Fore.RESET}"
            )
            .lower()
            .strip()
        )
        quit_check(user_input)
        if user_input == "":
            print(f"{Fore.GREEN}Skipping...{Fore.RESET}")
            return None
        try:
            num: int = int(user_input)
            if num < 1:
                print(
                    f"{Fore.RED}Invalid input. "
                    f"Please enter an integer greater than 0.{Fore.RESET}"
                )
                continue
            break
        except ValueError:
            print(
                f"{Fore.RED}Invalid input. "
                f"Please enter an integer greater than 0.{Fore.RESET}"
            )
    return num


def get_float(message: str) -> float:
    while True:
        user_input = input(message).lower().strip()
        quit_check(user_input)
        try:
            return float(user_input)
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid number.{Fore.RESET}")


def get_int(message: str, pos: bool = False) -> int:  # noqa: FBT001, FBT002
    while True:
        user_input = input(message).lower().strip()
        quit_check(user_input)
        try:
            num: int = int(user_input)
            if (num < 1) and pos:
                print(f"{Fore.RED}Please enter a number greater than 1.{Fore.RESET}")
                continue
            break
        except ValueError:
            print(
                f"{Fore.RED}Invalid input. "
                f"Please enter a valid whole number.{Fore.RESET}"
            )
    return num


allowed_operators: dict[Any, Callable[..., Any]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_eval(expr: str) -> float:
    try:
        tree: ast.Expression = ast.parse(expr, mode="eval")

        def eval_node(node) -> float:
            # numeric constants
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Only numeric constants are allowed.")

            # binary operations (+, -, *, /)
            elif isinstance(node, ast.BinOp):
                if type(node.op) not in allowed_operators:
                    raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
                left = eval_node(node.left)
                right = eval_node(node.right)
                return allowed_operators[type(node.op)](left, right)

            # unary operations (+, -)
            elif isinstance(node, ast.UnaryOp):
                if type(node.op) not in allowed_operators:
                    raise ValueError(
                        f"Unsupported unary operator: {type(node.op).__name__}"
                    )
                operand = eval_node(node.operand)
                return allowed_operators[type(node.op)](operand)

            # any other node type is disallowed
            else:
                raise ValueError(f"Unsupported syntax: {type(node).__name__}")

        return eval_node(tree.body)

    except Exception as e:
        raise ValueError(e)


def get_expr(message: str) -> float:
    while True:
        user_input = input(message).lower().strip()
        quit_check(user_input)
        try:
            return float(user_input)
        except ValueError:
            pass
        try:
            num = safe_eval(user_input)
            num = float(num)
            print(f"Evaluation: {num:.6f}")
            break
        except ValueError:
            print(
                f"{Fore.RED}Invalid input. Please enter a valid expression.{Fore.RESET}"
            )
    return num


days: dict[str, int] = {
    "sunday": 0,
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6,
}


def get_day(message: str) -> int:
    while True:
        user_input = input(message).lower().strip()
        quit_check(user_input)
        if user_input in days:
            return days[user_input]
        try:
            num: int = int(user_input)
            if num < 0 or num > 6:  # noqa: PLR2004
                print(
                    f"{Fore.RED}Please enter a number 0-6, "
                    f"or a day of the week.{Fore.RESET}"
                )
                continue
            break
        except ValueError:
            print(f"{Fore.RED}Invalid input.{Fore.RESET}")
    return num


def enter_to_cont() -> None:
    q: str = (
        input(
            f"{Fore.CYAN}Press {Fore.YELLOW}Enter{Fore.CYAN} "
            f"to continue...\n{Fore.RESET}"
        )
        .strip()
        .lower()
    )
    quit_check(q)


def in_bounds(test: float, lower: float, upper: float, include: bool) -> bool:  # noqa: FBT001
    if include:
        return test >= lower and test <= upper
    return test > lower and test < upper
