from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Button, Digits, Input, Label, Static


class QuestionNumber(Horizontal):
    current = reactive(0)

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
    def update_question(self, left: float, right: float, op: str) -> None:
        self.update(f"{left} {op} {right}")


class AnswerBox(Horizontal):
    def compose(self) -> ComposeResult:
        self.answer_box = Input(type="number", placeholder="Answer")
        self.submit_button = Button("Submit", disabled=True)
        yield self.answer_box
        yield self.submit_button

    @on(Input.Changed)
    def check_button(self) -> None:
        if self.answer_box.value:
            self.submit_button.disabled = False
        else:
            self.submit_button.disabled = True


class MathQuestion(Vertical):
    user_is_correct = reactive(False)

    def compose(self) -> ComposeResult:
        self.question_display = QuestionDisplay()
        yield self.question_display

    class CorrectAnswer(Message):
        bubble = True

    def watch_user_is_correct(self) -> None:
        self.post_message(self.CorrectAnswer())

    def new(self): ...

    def _check_answer(self): ...
