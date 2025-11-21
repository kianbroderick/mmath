from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Footer

from mmath.config import CONFIG
from mmath.questions.data_screen import EndScreen
from mmath.questions.question_widgets import QuestionUI


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
        selected = await self.app.push_screen_wait(EndScreen(self.qui.answer_data))
        if selected == "yes_repeat":
            self.qui.question_number.current = 0
            self.qui.new_question()
        else:
            self.app.pop_screen()


class QuestionScreenTest(App):
    CSS_PATH = "questionui.tcss"

    def compose(self) -> ComposeResult:
        self.qui = QuestionUI({"addition": 3}, 3)
        yield self.qui


if __name__ == "__main__":
    QuestionScreenTest().run()
