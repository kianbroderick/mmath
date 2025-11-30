from typing import TYPE_CHECKING, ClassVar

from textual.screen import Screen
from textual.widgets import Footer

from mentalmath.data.data_screen import EndScreen
from mentalmath.questions.question_widgets import QuestionUI

if TYPE_CHECKING:
    from textual.app import ComposeResult
    from textual.binding import BindingType


class QuestionScreen(Screen):
    BINDINGS: ClassVar[list[BindingType]] = [
        ("escape", "back_to_menu", "Back to menu"),
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def __init__(
        self,
        question_maxes: dict[str, int],
        number_of_questions: int,
        timer: str | None,
        vanish: str | None = None,
        special: int | None = None,
    ) -> None:
        super().__init__()
        self.question_maxes = question_maxes
        self.number_of_questions = number_of_questions
        self.timer = timer
        self.vanish = vanish
        self.special = special

    CSS_PATH = "../styles/questionui.tcss"

    def compose(self) -> ComposeResult:
        self.qui = QuestionUI(
            self.question_maxes,
            self.number_of_questions,
            self.timer,
            vanish=self.vanish,
            special=self.special,
        )
        yield self.qui
        yield Footer()

    async def on_question_ui_finished(self) -> None:
        selected = await self.app.push_screen_wait(EndScreen(self.qui.answer_data))
        if selected == "yes_repeat":
            self.qui.question_number.current = 0
            self.qui.new_question()
            self.qui.update_timer.resume()
        else:
            self.app.pop_screen()

    def action_back_to_menu(self) -> None:
        self.app.pop_screen()
