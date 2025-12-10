import random
import time
from typing import TYPE_CHECKING

from textual import on
from textual.containers import Center
from textual.message import Message
from textual.reactive import reactive
from textual.validation import Number
from textual.widget import Widget
from textual.widgets import Button, Digits, Input, ProgressBar, Static

if TYPE_CHECKING:
    from textual.app import ComposeResult


from mentalmath.config import CONFIG
from mentalmath.operations import AnswerData


class QuestionNumber(Widget):
    DEFAULT_CSS = """
        QuestionNumber {
        height: auto;
        width: auto;
        }
    """
    current = reactive(0)
    finished = reactive(False)

    def compose(self) -> ComposeResult:
        self.question_number = Digits(f"{0}")
        yield self.question_number

    def on_mount(self) -> None:
        self.question_number.border_title = "Question"

    def watch_current(self, new: int) -> None:
        self.question_number.update(str(new))

    def next(self) -> None:
        self.current += 1


class QuestionDisplay(Static):
    DEFAULT_CSS = """
        QuestionDisplay {
        width: auto;
    }
    """


class AnswerBox(Widget):
    DEFAULT_CSS = """
        AnswerBox {
        width: auto;
        }
    """

    def compose(self) -> ComposeResult:
        self.answer_box = Input(
            type="number", placeholder="Answer", validators=[Number()]
        )
        self.submit_button = Button("Submit", disabled=True, classes="next_button")
        yield self.answer_box
        yield self.submit_button

    @on(Input.Changed)
    def check_button(self) -> None:
        if self.answer_box.is_valid:
            self.submit_button.disabled = False
        else:
            self.submit_button.disabled = True


def in_bounds(test: float, bounds: tuple[float, float]) -> bool:
    lower, upper = bounds
    return test >= lower and test <= upper


class QuestionUI(Widget):
    timer = reactive(0.0)
    start_time = reactive(time.monotonic)
    time_at_last_err = reactive(time.monotonic)
    time_since_last_err = reactive(0.0)

    def __init__(
        self,
        op_maxes: dict[str, int],
        number_of_questions: int,
        timer: str | None,
        vanish: str | None = None,
        special: int | None = None,
    ) -> None:
        super().__init__()
        self.op_maxes = op_maxes
        self.number_of_questions = number_of_questions
        self.question_timer = float(timer) if timer else None
        self.vanish = float(vanish) if vanish else None
        self.answer_data: dict[int, AnswerData] = {}
        self.special = special
        self.add_class("question-ui")

    def compose(self) -> ComposeResult:
        self.question_number = QuestionNumber()
        self.question_display = QuestionDisplay()
        self.answer_box = AnswerBox()
        yield self.question_number
        yield Center(self.question_display)
        with Center():
            yield ProgressBar(
                total=self.question_timer,
                show_eta=False,
                show_percentage=False,
            )
        yield self.answer_box

    def on_mount(self) -> None:
        if not self.question_timer:
            self.query_one(ProgressBar).visible = False
        self.new_question()
        self.update_timer = self.set_interval(1 / 100, self.update_time)

    def update_time(self) -> None:
        """Method to update time to current."""
        self.timer = time.monotonic() - self.start_time
        self.time_since_last_err = time.monotonic() - self.time_at_last_err

    def reset_timer(self) -> None:
        """Method to update time to current."""
        self.timer = 0.0
        self.start_time = time.monotonic()
        self.time_since_last_err = 0.0
        self.time_at_last_err = time.monotonic()

    def watch_timer(self, time: float) -> None:
        """If the user set a timer, move to the next question when time is up."""
        bar = self.query_one(ProgressBar)
        bar.update(progress=time)
        if self.question_timer:
            if time < 0.75 * self.question_timer:
                bar.remove_class("ending")
                bar.add_class("normal")
            elif time < self.question_timer:
                bar.remove_class("normal")
                bar.add_class("ending")
            elif time > self.question_timer:
                bar.remove_class(*["normal", "ending"])
                self.out_of_time()
        if self.vanish:
            if self.time_since_last_err > self.vanish:
                self.question_display.update("")
            else:
                self.question_display.update(self.question.display)

    def new_question_data(self) -> None:
        operation = random.choice(list(self.op_maxes.keys()))
        top = self.op_maxes[operation]
        cls = CONFIG.ALLOPERATIONS[operation]
        self.question = cls(num=self.special)
        self.question.new(top)
        self.answer_box.answer_box.restrict = self.question.input_restrictions
        self.answer_box.answer_box.type = self.question.textual_input_type

    class Finished(Message): ...

    def check_finished(self) -> bool:
        if self.question_number.current == self.number_of_questions:
            self.post_message(self.Finished())
            self.update_timer.pause()
            return True
        return False

    def new_question(self) -> None:
        if self.check_finished():
            return
        self.question_number.next()
        self.n_err = 0
        self.new_question_data()
        self.question_display.update(self.question.display)
        self.reset_timer()

    def flash_class(
        self, widget: Widget, class_name: str, duration: float = 0.15
    ) -> None:
        widget.add_class(class_name)
        self.set_timer(duration, lambda: widget.remove_class(class_name))

    @on(Input.Submitted)
    @on(Button.Pressed)
    def check_submission(self) -> None:
        submission = self.answer_box.answer_box.value
        if not submission:
            self.answer_box.answer_box.clear()
            return
        if self.question.verify_correct(submission):
            self.flash_class(self.answer_box.answer_box, "correct")
            self.flash_class(self.question_display, "correct")
            self.flash_class(self.question_number, "correct")
            self.flash_class(self, "correct")
            self.answer_box.answer_box.clear()
            qdata = self.question
            answerdata = AnswerData(
                qdata.symbol,
                qdata.left,
                qdata.right,
                self.timer,
                self.n_err,
                out_of_time=False,
            )
            self.answer_data[self.question_number.current] = answerdata
            self.new_question()
        else:
            self.answer_box.answer_box.clear()
            self.time_at_last_err = time.monotonic()
            self.flash_class(self.answer_box.answer_box, "incorrect")
            self.flash_class(self.question_display, "incorrect")
            self.flash_class(self.question_number, "incorrect")
            self.flash_class(self, "incorrect")
            self.n_err += 1

    def out_of_time(self) -> None:
        self.answer_box.answer_box.clear()
        self.flash_class(self.answer_box.answer_box, "incorrect")
        self.flash_class(self.question_display, "incorrect")
        self.flash_class(self.question_number, "incorrect")
        self.flash_class(self, "incorrect")
        qdata = self.question
        answerdata = AnswerData(
            qdata.symbol,
            qdata.left,
            qdata.right,
            min(self.timer, self.question_timer),
            self.n_err,
            out_of_time=True,
        )
        self.answer_data[self.question_number.current] = answerdata
        self.new_question()
