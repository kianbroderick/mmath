import random
import time
from typing import TYPE_CHECKING

from textual import on
from textual.message import Message
from textual.reactive import reactive
from textual.validation import Number
from textual.widget import Widget
from textual.widgets import Button, Digits, Input, Label, Static

if TYPE_CHECKING:
    from textual.app import ComposeResult

    from mmath.questions.operations import QuestionData

from mmath.config import CONFIG
from mmath.questions.operations import AnswerData


class QuestionNumber(Widget):
    DEFAULT_CSS = """
        QuestionNumber {
        height: auto;
        }
    """
    current = reactive(0)
    finished = reactive(False)

    def compose(self) -> ComposeResult:
        self.question_number_label = Label("Question")
        self.question_number = Digits(f"{0}")
        yield self.question_number_label
        yield self.question_number

    def watch_current(self, new: int) -> None:
        self.question_number.update(str(new))

    def next(self) -> None:
        self.current += 1


class QuestionDisplay(Static):
    pass


class AnswerBox(Widget):
    def compose(self) -> ComposeResult:
        self.answer_box = Input(
            type="number", placeholder="Answer", validators=[Number()]
        )
        self.submit_button = Button("Submit", disabled=True)
        yield self.answer_box
        yield self.submit_button

    @on(Input.Changed)
    def check_button(self) -> None:
        if self.answer_box.is_valid:
            self.submit_button.disabled = False
        else:
            self.submit_button.disabled = True


class QuestionUI(Widget):
    def __init__(self, op_maxes: dict[str, int], number_of_questions: int) -> None:
        super().__init__()
        self.op_maxes = op_maxes
        self.number_of_questions = number_of_questions
        self.answer_data: dict[int, AnswerData] = {}

    def compose(self) -> ComposeResult:
        self.question_number = QuestionNumber()
        self.question_display = QuestionDisplay()
        self.answer_box = AnswerBox()
        yield self.question_number
        yield self.question_display
        yield self.answer_box

    def on_mount(self) -> None:
        self.new_question()

    def new_question_data(self) -> QuestionData:
        operation = random.choice(list(self.op_maxes.keys()))
        top = self.op_maxes[operation]
        return CONFIG.QUESTIONDATA[operation](top)

    class Finished(Message): ...

    def check_finished(self) -> None:
        if self.question_number.current == self.number_of_questions:
            self.post_message(self.Finished())

    def new_question(self) -> None:
        self.question_number.next()
        self.n_err = 0
        self.q_data = self.new_question_data()
        self.question_display.update(self.q_data.display)
        self.time = time.time()

    @on(Input.Submitted)
    @on(Button.Pressed)
    def check_submission(self) -> None:
        submission = self.answer_box.answer_box.value
        if not submission:
            self.answer_box.answer_box.clear()
            return
        if int(self.answer_box.answer_box.value) == self.q_data.correct:
            self.answer_box.answer_box.clear()
            self.time = time.time() - self.time
            qdata = self.q_data
            answerdata = AnswerData(
                qdata.name, qdata.left, qdata.right, self.time, self.n_err
            )
            self.answer_data[self.question_number.current] = answerdata
            self.check_finished()
            self.new_question()
        else:
            self.n_err += 1
