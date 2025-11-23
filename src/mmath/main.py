from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Center
from textual.widget import Widget
from textual.widgets import Button, Footer, Input, Static

from mmath.config import CONFIG
from mmath.menus.mainmenu import MainMenu
from mmath.menus.maxes_screen import InputMaxesScreen
from mmath.questions.question_screen import QuestionScreen
from mmath.special.special_screen import SelectSpecialScreen


class Logo(Static):
    DEFAULT_CSS = """
        Logo {
            content-align: center middle;
            height: auto;   /* works because Static auto-sizes */
        }
    """
    logo = """[bold][blue]


                              __   __
    .--------.--------.---.-.|  |_|  |--.
    |        |        |  _  ||   _|     |
    |__|__|__|__|__|__|___._||____|__|__|
[/bold][/blue]
"""

    def render(self) -> str:
        return self.logo


class MentalMathApp(App):
    CSS_PATH = "styles/main.tcss"

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        self.mainmenu = MainMenu(id="mainmenu")
        yield Center(Logo(id="logo"))
        yield self.mainmenu
        yield Footer()

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    @work
    @on(Button.Pressed)
    async def user_maxes(self, event: Button.Pressed) -> None:
        """Opens the configure maxes screen."""
        if event.button.id == "next_button_to_maxes":
            await self.configure_maxes()
            await self.start_quiz()

    @work
    @on(Input.Submitted)
    async def numq_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "input_number_of_questions":
            if not self.mainmenu.next_button.disabled:
                await self.configure_maxes()
                await self.start_quiz()

    async def configure_maxes(self) -> None:
        screen = InputMaxesScreen(self.mainmenu.ops.selection_list.selected)
        self.operation_maxes = await self.push_screen_wait(screen)

    async def start_quiz(self) -> None:
        """Pushes the QuestionScreen with the operation_maxes and numq"""
        number_of_questions = int(self.mainmenu.input_numq.value)
        self.clear_screen()
        await self.push_screen_wait(
            QuestionScreen(self.operation_maxes, number_of_questions)
        )

    def clear_screen(self) -> None:
        self.mainmenu.ops.selection_list.deselect_all()
        self.mainmenu.input_numq.clear()

    @on(Button.Pressed)
    def go_to_specials(self, event: Button.Pressed) -> None:
        if event.button.id == "go_to_specials":
            self.push_screen(SelectSpecialScreen())


app = MentalMathApp()


def main() -> None:
    app = MentalMathApp()
    app.run()


if __name__ == "__main__":
    main()
