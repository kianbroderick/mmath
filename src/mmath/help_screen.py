from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widgets import Collapsible, Footer, Markdown, Tabs

TABNAMES = [
    "help",
    "square root",
    "fraction",
    "complex",
]

MMATH_MAIN_MD = """\
# mmath
A mental math training app
"""

GET_STARTED_MD = """\
Here is where I will introduce the app and it's features.
"""

ARITHMETIC_MD = """\
Here is where I will describe addition, subtraction, multiplication.
"""

FRACTIONS_MD = """\
Here is where I will describe how to do fractions
"""

COMPLEX_MD = """\
describing complex numbers
"""

CONVERSIONS_MD = """\
describing the conversions
"""

CALENDAR_MD = """\
describing the calender
"""

SPECIAL_MD = """\
describing the special screen
"""


class Content(VerticalScroll, can_focus=False): ...


class HelpScreen(ModalScreen):
    CSS_PATH = "styles/help_screen.tcss"
    BINDINGS = [("q,b,h", "close", "Close")]

    def compose(self) -> ComposeResult:
        with Content():
            yield Markdown(MMATH_MAIN_MD)
            with Collapsible(title="Get Started", collapsed=False):
                yield Markdown(GET_STARTED_MD)
            with Collapsible(title="Arithmetic"):
                yield Markdown(ARITHMETIC_MD)
            with Collapsible(title="Fractions"):
                yield Markdown(FRACTIONS_MD)
            with Collapsible(title="Complex"):
                yield Markdown(COMPLEX_MD)
            with Collapsible(title="Unit Conversions"):
                yield Markdown(CONVERSIONS_MD)
            with Collapsible(title="Calendar"):
                yield Markdown(CALENDAR_MD)
            with Collapsible(title="Special"):
                yield Markdown(SPECIAL_MD)
        yield Footer()

    def action_close(self) -> None:
        self.app.pop_screen()
