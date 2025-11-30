from typing import TYPE_CHECKING, ClassVar

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Center
from textual.theme import Theme
from textual.widgets import Button, Footer, Input, Static

from mentalmath.menus.mainmenu import MainMenu
from mentalmath.menus.maxes_screen import InputMaxesScreen
from mentalmath.questions.question_screen import QuestionScreen
from mentalmath.special.special_screen import SelectSpecialScreen

if TYPE_CHECKING:
    from textual.binding import BindingType


class Logo(Static):
    DEFAULT_CSS = """
        Logo {
            content-align: center middle;
            height: auto;
        }
    """
    logo = """[bold]
                          __   __
.--------.--------.---.-.|  |_|  |--.
|        |        |  _  ||   _|     |
|__|__|__|__|__|__|___._||____|__|__|
[/bold]
"""

    def render(self) -> str:
        return self.logo


mmath_theme = Theme(
    name="mmath",
    primary="#30C5FF",
    secondary="#A0DDE6",
    accent="#5C946E",
    foreground="#D8DEE9",
    background="#2A2D34",
    success="#D2FF28",
    warning="#FF6F59",
    error="#B80C09",
    surface="#3B4252",
    panel="#427AA1",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
    },
)


class MentalMathApp(App):
    CSS_PATH = "styles/main.tcss"

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        self.mainmenu = MainMenu(id="mainmenu")
        yield Center(Logo(id="logo"))
        yield self.mainmenu
        yield Footer()

    def on_mount(self) -> None:
        # Register the theme
        self.register_theme(mmath_theme)

        # Set the app's theme
        self.theme = "mmath"

    BINDINGS: ClassVar[list[BindingType]] = [
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
        if (
            event.input.id == "input_number_of_questions"
            and not self.mainmenu.next_button.disabled
        ):
            await self.configure_maxes()
            await self.start_quiz()

    async def configure_maxes(self) -> None:
        screen = InputMaxesScreen(self.mainmenu.ops.selection_list.selected)
        self.operation_maxes, self.timer, self.vanish = await self.push_screen_wait(
            screen
        )

    async def start_quiz(self) -> None:
        """Pushes the QuestionScreen with the operation_maxes and numq"""
        number_of_questions = int(self.mainmenu.input_numq.value)
        self.clear_screen()
        await self.push_screen_wait(
            QuestionScreen(
                self.operation_maxes,
                number_of_questions,
                self.timer,
                vanish=self.vanish,
            )
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
