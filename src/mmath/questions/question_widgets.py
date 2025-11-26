import random
import time
from typing import TYPE_CHECKING

from textual import on
from textual.containers import Center
from textual.message import Message
from textual.reactive import reactive
from textual.validation import Number
from textual.widget import Widget
from textual.widgets import Button, Digits, Input, Label, Static

if TYPE_CHECKING:
    from textual.app import ComposeResult

    from mmath.operations import QuestionData

from mmath.config import CONFIG
from mmath.operations import AnswerData, QuestionInfo


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
    def __init__(self, op_maxes: dict[str, int], number_of_questions: int) -> None:
        super().__init__()
        self.op_maxes = op_maxes
        self.number_of_questions = number_of_questions
        self.answer_data: dict[int, AnswerData] = {}
        self.add_class("question-ui")

    def compose(self) -> ComposeResult:
        self.question_number = QuestionNumber()
        self.question_display = QuestionDisplay()
        self.answer_box = AnswerBox()
        yield self.question_number
        yield Center(self.question_display)
        yield self.answer_box

    def on_mount(self) -> None:
        self.new_question()

    def new_question_data(self) -> None:
        operation = random.choice(list(self.op_maxes.keys()))
        top = self.op_maxes[operation]
        cls = CONFIG.QUESTIONDATA[operation]
        self.question = cls()
        self.question.new(top)
        self.answer_box.answer_box.restrict = self.question.input_restrictions
        self.answer_box.answer_box.type = self.question.textual_input_type

    class Finished(Message): ...

    def check_finished(self) -> bool:
        if self.question_number.current == self.number_of_questions:
            self.post_message(self.Finished())
            return True
        else:
            return False

    def new_question(self) -> None:
        if self.check_finished():
            return
        self.question_number.next()
        self.n_err = 0
        self.new_question_data()
        self.question_display.update(self.question.display)
        self.time = time.time()

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
            self.time = time.time() - self.time
            qdata = self.question
            answerdata = AnswerData(
                qdata.symbol, qdata.left, qdata.right, self.time, self.n_err
            )
            self.answer_data[self.question_number.current] = answerdata
            self.new_question()
        else:
            self.answer_box.answer_box.clear()
            self.flash_class(self.answer_box.answer_box, "incorrect")
            self.flash_class(self.question_display, "incorrect")
            self.flash_class(self.question_number, "incorrect")
            self.flash_class(self, "incorrect")
            self.n_err += 1
