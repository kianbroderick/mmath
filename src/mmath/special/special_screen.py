from typing import TYPE_CHECKING

from textual import on, work
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Button, Footer

from mmath.config import CONFIG
from mmath.operations import default
from mmath.questions.question_screen import QuestionScreen
from mmath.special.num_questions_screen import NumberOfQuestionsScreen
from mmath.special.powers import ConfigurePowersScreen
from mmath.special.times_tables import ConfigureTimesTablesScreen, TimesTableScreen

if TYPE_CHECKING:
    from textual.app import ComposeResult


def convert_snake_case(string: str) -> str:
    return string.replace("_", " ").title()


class SelectSpecialScreen(Screen):
    SCOPED_CSS = True
    CSS_PATH = "../styles/special_screen.tcss"
    BINDINGS = [("b", "go_back", "Back")]

    def compose(self) -> ComposeResult:
        with Grid(id="special_grid"):
            for special in list(CONFIG.SPECIAL.keys()):
                title = convert_snake_case(special)
                yield Button(
                    title,
                    id=f"{special}_button",
                    classes="special_button",
                )
        yield Button("Back", classes="back_button")
        yield Footer()

    @work
    @on(Button.Pressed)
    async def config_times_tables(self, event: Button.Pressed) -> None:
        if event.button.id == "times_tables_button":
            await self.app.push_screen_wait(ConfigureTimesTablesScreen())
        if event.button.id == "powers_button":
            await self.app.push_screen_wait(ConfigurePowersScreen())
        if event.button.id == "default_button":
            num_q, timer, vanish = await self.app.push_screen_wait(
                NumberOfQuestionsScreen()
            )
            self.app.push_screen(QuestionScreen(default, num_q, timer, vanish=vanish))
        if event.button.id == "calendar_button":
            num_q, timer, vanish = await self.app.push_screen_wait(
                NumberOfQuestionsScreen()
            )
            self.app.push_screen(
                QuestionScreen(
                    {"calendar": 1}, num_q, timer, vanish=vanish, special=None
                )
            )
        elif "back_button" in event.button.classes:
            self.app.pop_screen()

    def action_go_back(self) -> None:
        self.app.pop_screen()
