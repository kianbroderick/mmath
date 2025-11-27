from textual import events
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widget import Widget
from textual.widgets import Collapsible, Footer, Label, Markdown, Static, Tab, Tabs

TABNAMES = [
    "help",
    "square root",
    "fraction",
    "complex",
]

MMATH_MAIN_MD = """\
# mmath
A mental math training application. Practice your arithmetic, unit conversions, and more.
Use **tab** and **shift+tab** to jump through the menus.
"""

GET_STARTED_MD = """\
From the main menu, use **enter** or **space** to select which operations you wish to practice. \
Then enter your desired number of questions, and after hitting **next** you will arrive at the configuration screen. \
You will enter the maximum number you wish to calculate for that operation. \
For example, entering '999' for addition will let you practice three digit addition. \
Pressing **submit** will send you to the quiz screen, where you will have to answer the questions. \
After the quiz, you will see an end screen containing statistics about your quiz, and you can view the data more in-depth by pressing **d**.
"""

ARITHMETIC_MD = """\
**Addition**, **subtraction**, **multiplication**, and **square** are self-explanatory. You must enter the exact integer solution. \
**Mod** requires you to calculate the remainder of the number on the left when divided by the number on the right. \
For example, 22 mod 10 is equal to 2.
"""

FRACTIONS_MD = """\
**Fraction addition** and **multiplication** requires you to enter the sum or product in the most simplified form. \
Enter your solution as 'numerator / denominator'.
"""

COMPLEX_MD = """\
**Complex multiplication** of two complex numbers a + bi and c + di is computed as \n
(a + b\\*i) * (c + d\\*i) = (a*c - b*d) + (a*d + b*c)*i. \n
Enter your solution as a sum of the real part and the imaginary part. The real part must come first, \
and you may use **i**,** I**,** j**, or **J** as the imaginary unit. The multiplication sign between the imaginary part and **i** is optional.
"""

SQUARE_ROOT_MD = """\
"""

CONVERSIONS_MD = """\
Each **unit conversion** allows for a range of correct solutions. \
You must answer within 1% of the interval defined by the exact solution and the mental approximation. \
The upper bound and lower bounds and rounded up and down to the nearest integer, respectively. \n
**Pounds to Kilograms**\n
Exact: kg = 0.4535924 * lb\n
Approx: kg = 0.45 * lb, or divide by 2 and subtract 10%\n

**Pounds to Kilograms**\n
Exact: kg = 0.4535924 * lb\n
Approx: kg = 0.45 * lb, or divide by 2 and subtract 10%\n
**Kilograms to Pounds**\n
Exact: lb = 2.204623 * kg\n
Approx: kg = 2.2 * lb, or multiply by 2 and add 10%\n
**Miles to Kilometers**\n
Exact: km = 0.6213712 * mi\n
Approx: km = 0.625 * mi, or divide by 8 and multiply by 5\n
**Miles to Kilometers**\n
Exact: mi = 1.609344 * km\n
Approx: km = 1.6 * mi, or multiply by 8 and divide by 5\n
**Celsius to Fahrenheit**\n
Exact: C = F * 1.8 + 32\n
Approx: C = F * 2 + 30\n
**Fahrenheit to Celsius**\n
Exact: F = (C - 32) / 1.8\n
Approx: F = (C - 30) / 2\n
"""

CALENDAR_MD = """\
Coming soon...
"""

SPECIAL_MD = """\
Selecting **special** from the menu screen takes you to the specials screen. \n
**Times tables** allows you to enter a specific number and practice its times table. \
Choose the number you want to practice, and the value you want to practice up to. \n
**Default** is three digit addition and subtraction and two digit multiplication, squaring, and square roots.

"""

DISTANCE_CONV = [
    """
**Miles to Kilometers**\n
Exact: km = 0.6213712 * mi\n
Approx: km = 0.625 * mi, or divide by 8 and multiply by 5\n
""",
    """
**Miles to Kilometers**\n
Exact: mi = 1.609344 * km\n
Approx: km = 1.6 * mi, or multiply by 8 and divide by 5\n
""",
]


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
            with Collapsible(title="Square Root"):
                yield Markdown(SQUARE_ROOT_MD)
            with Collapsible(title="Unit Conversions"):
                yield Markdown(CONVERSIONS_MD)
            with Collapsible(title="Calendar"):
                yield Markdown(CALENDAR_MD)
            with Collapsible(title="Special"):
                yield Markdown(SPECIAL_MD)
        yield Footer()

    def action_close(self) -> None:
        self.app.pop_screen()
