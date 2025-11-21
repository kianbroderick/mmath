from typing import TYPE_CHECKING

from textual import on, work
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Button, Footer

from mmath.config import CONFIG
from mmath.special.times_tables import ConfigureTimesTablesScreen, TimesTableScreen

if TYPE_CHECKING:
    from textual.app import ComposeResult


class SelectSpecialScreen(Screen):
    def compose(self) -> ComposeResult:
        with Grid():
            for special in list(CONFIG.SPECIAL.keys()):
                yield Button(special, id=f"{special}_button")
        yield Button("Back", classes="back_button")
        yield Footer()

    @work
    @on(Button.Pressed)
    async def config_times_tables(self, event: Button.Pressed) -> None:
        if event.button.id == "times_tables_button":
            await self.app.push_screen_wait(ConfigureTimesTablesScreen())
        elif "back_button" in event.button.classes:
            self.app.pop_screen()
