import random
import time
from statistics import mean, median, stdev

from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical
from textual.message import Message
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, DataTable, Footer, Label

from mmath.config import CONFIG
from mmath.questions.data_screen import DataScreen, QuestionData
from mmath.questions.question_widgets import AnswerBox, QuestionDisplay, QuestionNumber


class EndScreen(ModalScreen):
    """Screen where you can get data, restart, or go back to mainmenu."""

    BINDINGS = CONFIG.DEFAULT_BINDINGS

    def __init__(self, data: dict[int, QuestionData]) -> None:
        super().__init__()
        self.data = data

    def compose(self) -> ComposeResult:
        self.summary_table = DataTable()
        yield self.summary_table
        yield Grid(
            Label("Repeat?", id="question"),
            Button("Data", id="view_data_button"),
            Button("No", variant="error", id="no_repeat"),
            Button("Yes", variant="primary", id="yes_repeat"),
            id="dialog",
        )
        yield Footer()

    def on_mount(self) -> None:
        times = [x.time for x in self.data.values()]
        average = mean(times)
        std_dev = stdev(times) if len(times) > 1 else 0
        data_median = median(times)
        minimum = min(times)
        maximum = max(times)
        data_range = maximum - minimum
        self.summary_table.add_columns(
            "average", "standard deviation", "median", "minimum", "maximum", "range"
        )
        self.summary_table.add_row(
            average, std_dev, data_median, minimum, maximum, data_range
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "view_data_button":
            self.app.push_screen(DataScreen(data=self.data))
        else:
            self.dismiss(event.button.id)


class QuestionUI(Vertical):
    def __init__(self, op_maxes: dict[str, int], number_of_questions: int) -> None:
        super().__init__()
        self.op_maxes = op_maxes
        self.number_of_questions = number_of_questions
        self.question_data: dict[int, QuestionData] = {}

    def compose(self) -> ComposeResult:
        self.question_number = QuestionNumber()
        self.question_display = QuestionDisplay()
        self.answer_box = AnswerBox(id="question_answer_box")
        yield self.question_number
        yield self.question_display
        yield self.answer_box

    def on_mount(self) -> None:
        self.new_question()
        self.question_display.update_question(
            self.left, self.right, CONFIG.SYMBOLS[self.operation_name]
        )

    def new_question(self) -> None:
        # self.operation is the callable function
        self.operation_name = random.choice(list(self.op_maxes.keys()))
        self.operation = CONFIG.OPERATIONS[self.operation_name]
        self.left = random.randint(1, self.op_maxes[self.operation_name])
        self.right = random.randint(1, self.op_maxes[self.operation_name])
        self.correct_answer = self.operation(self.left, self.right)
        self.question_display.update_question(
            self.left, self.right, CONFIG.SYMBOLS[self.operation_name]
        )
        self.question_number.next()
        self.question_data[self.question_number.current] = QuestionData(
            self.operation_name, self.left, self.right, time.time(), 0
        )

    class Finished(Message, bubble=True):
        """Finished quiz message."""

    def _check_answer(self) -> None:
        user_answer = self.answer_box.answer_box.value
        if not user_answer:
            return
        if int(user_answer) == self.correct_answer:
            this_question_data = self.question_data[self.question_number.current]
            start_time = this_question_data.time
            this_question_data.time = time.time() - start_time
            self._check_finished()
        else:
            self.question_data[self.question_number.current].number_of_errors += 1

    def _check_finished(self) -> None:
        if self.question_number.current == self.number_of_questions:
            self.post_message(self.Finished())
        else:
            self.new_question()

    def on_input_submitted(self) -> None:
        self._check_answer()
        self.answer_box.answer_box.clear()

    def on_button_pressed(self) -> None:
        self._check_answer()
        self.answer_box.answer_box.clear()


class QuestionScreen(Screen):
    BINDINGS = CONFIG.DEFAULT_BINDINGS

    def __init__(
        self, question_maxes: dict[str, int], number_of_questions: int
    ) -> None:
        super().__init__()
        self.question_maxes = question_maxes
        self.number_of_questions = number_of_questions

    CSS_PATH = "questionui.tcss"

    def compose(self) -> ComposeResult:
        self.qui = QuestionUI(self.question_maxes, self.number_of_questions)
        yield self.qui
        yield Footer()

    async def on_question_ui_finished(self) -> None:
        selected = await self.app.push_screen_wait(EndScreen(self.qui.question_data))
        if selected == "yes_repeat":
            self.qui.question_number.current = 0
            self.qui.new_question()
        else:
            self.app.pop_screen()


class QuestionScreenTest(App):
    CSS_PATH = "questionui.tcss"

    def compose(self) -> ComposeResult:
        self.qui = QuestionUI({"multiplication": 3}, 3)
        yield self.qui


if __name__ == "__main__":
    QuestionScreenTest().run()
