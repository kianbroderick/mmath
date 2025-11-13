import time
from collections.abc import Callable

from colorama import Fore

from config import (
    ALL_OPERATIONS,
    ROUNDING_NUM,
    configure,
    configure_custom,
    configure_powers,
    configure_times_tables,
    print_summary,
)
from operations import QuestionResult
from utils import (
    RestartProgram,
    get_int,
    get_str,
    print_ui,
)


class QuestionLog:
    def __init__(self) -> None:
        self.log: dict[
            tuple[str, str] | tuple[str, str, str], dict[str, float | int]
        ] = {}

    def update(self, data: QuestionResult) -> None:
        if data.question_info in self.log:
            new_time = (self.log[data.question_info]["time"] + data.question_time) / 2
            new_errors = self.log[data.question_info]["n_errors"] + data.num_wrong
            self.log[data.question_info] = {"time": new_time, "n_errors": new_errors}
        else:
            self.log[data.question_info] = {
                "time": data.question_time,
                "n_errors": data.num_wrong,
            }

    def print_data(self) -> None:
        sorted_questions = sorted(
            self.log.items(), key=lambda item: item[1]["time"], reverse=True
        )
        number_data = [item[0] for item in sorted_questions]

        q_times = [item[1]["time"] for item in sorted_questions]
        q_width: int = max(len(f"{x:.{ROUNDING_NUM}f}") for x in q_times)

        l_width: int = 0
        r_width: int = 0
        op_width: int = 0
        for data in number_data:
            l_width = max(l_width, len(str(data[1])))
            op_width = max(op_width, len(data[0]))
            if len(data) >= 3:  # noqa: PLR2004
                r_width = max(r_width, len(str(data[2])))
        for op_nums, result_dict in sorted_questions:
            op, *nums = op_nums
            a = nums[0]
            b = nums[1] if len(nums) == 2 else ""  # noqa: PLR2004
            print(
                f"{Fore.BLUE}{a:>{l_width}}"
                f"{Fore.YELLOW} {op:^{op_width}} "
                f"{Fore.BLUE}{b:<{r_width}}"
                f"{Fore.GREEN} | {result_dict['time']:>{q_width}.{ROUNDING_NUM}f}"
                f" seconds"
                f" | {Fore.RESET}",
                end="",
            )
            if result_dict["n_errors"] != 0:
                print(
                    f"{Fore.RED}{result_dict['n_errors']} error{Fore.RESET}",
                    end="",
                )
                if result_dict["n_errors"] > 1:
                    print(f"{Fore.RED}s{Fore.RESET}", end="")
            print()


def play_round(
    trial: Callable[[int], QuestionResult] | Callable[[], QuestionResult],
    num_q: int,
    *args: int,
) -> QuestionLog:
    total_errors: int = 0
    q_times: list[float] = []
    question_log = QuestionLog()
    start_round: float = time.time()
    for i in range(num_q):
        print_ui()
        print(f"{Fore.BLUE}Question {i + 1}\n{Fore.RESET}")
        trial_result = trial(*args)
        total_errors += trial_result.num_wrong
        q_times.append(trial_result.question_time)
        question_log.update(trial_result)
    end_round: float = time.time()
    print_ui()
    print_summary(num_q, total_errors, start_round, end_round, q_times)
    return question_log


def again_msg() -> None:
    print(
        "\n"
        f"{Fore.BLUE}Again? ("
        f"{Fore.GREEN}y"
        f"{Fore.BLUE}/"
        f"{Fore.RED}n"
        f"{Fore.BLUE}), or {Fore.YELLOW}d{Fore.BLUE} to view data.{Fore.RESET}"
    )


def main_loop(
    trial: Callable[[int], QuestionResult] | Callable[[], QuestionResult],
    num_q: int,
    *args: int,
) -> None:
    again: str = "y"
    while True:
        question_log = play_round(trial, num_q, *args)
        while True:
            again_msg()
            again = get_str()
            if again == "y":
                break
            if again == "n":
                return
            if again == "d":
                print()
                question_log.print_data()
            else:
                print(f"{Fore.RED}Invalid input.{Fore.RESET}")


# Special cases for the default and custom function
# as those have different ways of defining max number

type Trial = Callable[..., QuestionResult]

def main() -> None:
    try:
        while True:
            print_ui()
            op, num_q = configure()
            if op == "custom":
                trial: Trial = configure_custom()
                main_loop(trial, num_q)
                continue
            if op == "default":
                trial = ALL_OPERATIONS[op]
                main_loop(trial, num_q)
                continue
            if op == "cal":
                trial = ALL_OPERATIONS[op]
                main_loop(trial, num_q)
                continue
            if op == "pow":
                trial = configure_powers()
            elif op in {"times tables", "tt"}:
                trial = configure_times_tables()
            else:
                trial = ALL_OPERATIONS[op]
            print(f"{Fore.BLUE}What is the max number?{Fore.RESET}")
            top = get_int(f"{Fore.GREEN}Enter a number: {Fore.RESET}", pos=True)
            main_loop(trial, num_q, top)
    except RestartProgram:
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + f"{Fore.BLUE}Program interrupted. Exiting...{Fore.RESET}")
