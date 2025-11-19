from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import (
    Button,
    Footer,
)

from mmath.config import CONFIG
from mmath.menus.mainmenu import MainMenu
from mmath.menus.maxes_screen import InputMaxesScreen
from mmath.questions.question_screen import QuestionScreen


class MentalMathApp(App):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        self.mainmenu = MainMenu()
        yield self.mainmenu
        yield Footer()

    BINDINGS = CONFIG.DEFAULT_BINDINGS

    @work
    @on(Button.Pressed)
    async def user_maxes(self, event: Button.Pressed) -> None:
        """Opens the configure maxes screen."""
        if event.button.id == "next_button_to_maxes":
            screen = InputMaxesScreen(self.mainmenu.ops.selection_list.selected)
            self.operation_maxes = await self.push_screen_wait(screen)
            await self.start_quiz()

    async def start_quiz(self) -> None:
        """Pushes the QuestionScreen with the operation_maxes and numq"""
        await self.push_screen_wait(
            QuestionScreen(self.operation_maxes, int(self.mainmenu.input_numq.value))
        )


def main() -> None:
    app = MentalMathApp()
    app.run()


if __name__ == "__main__":
    main()
