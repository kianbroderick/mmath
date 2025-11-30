from typing import TYPE_CHECKING

from textual.containers import VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Collapsible, Footer, Markdown

if TYPE_CHECKING:
    from textual.app import ComposeResult

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
For example, entering '999' for **addition** will let you practice three digit addition. \
Pressing **submit** will send you to the quiz screen, where you will have to answer the questions. \
After the quiz, you will see an end screen containing statistics about your quiz, and you can view the data more in-depth by pressing **d**.
"""

TIMER_VANISH_MD = """\
You can optionally set a **timer** for each question or make the question **vanish** after a certain period. \
The timer will make the question automatically continue to the next question after the time is up, \
and will log the mistakes for that question as '9999'. Vanish will make the question disappear after a \
time limit. Entering an incorrect answer will make the question reappear.
"""

ARITHMETIC_MD = """\
**Addition**, **subtraction**, **multiplication**, and **square** are self-explanatory. You must enter the exact integer solution. \
**Mod** requires you to calculate the remainder of the number on the left when divided by the number on the right. \
For example, 22 mod 10 is equal to 2.
"""

DIVISION_MD = """\
**Division** has you calculate the quotient and remainder of a division question. \
You must answer in the form '**quotient r remainder**'. If there is no remainder, just writing the solution is accepted.
"""

FRACTIONS_MD = """\
**Fraction addition** and **multiplication** requires you to enter the sum or product in the most simplified form. \
The fractions in the question are in the most simplified form. \
Enter your solution as '**numerator / denominator**'.
"""

COMPLEX_MD = """\
**Complex multiplication** of two complex numbers a + bi and c + di is computed as \n
(a + b\\*i) * (c + d\\*i) = (a*c - b*d) + (a*d + b*c)*i. \n
Enter your solution as a sum of the real part and the imaginary part. The real part must come first, \
and you may use **i**, **I**, **j**, or **J** as the imaginary unit. The multiplication sign between the imaginary part and **i** is optional.
"""

SQUARE_ROOT_MD = """\
**Square root** asks you to calculate the square root of a given number. \
You must answer within 1% of the interval defined by the exact solution and the approximation after one iteration of the Newton-Raphson method. \
The upper and lower bounds are rounded up and down to the nearest integer, respectively. \
The **max** number is the maximum number to square root. \n
**Perfect square root** asks you to calculate the square root of a given perfect square. \
The exact integer solution is required. \
The **max** number is the maximum number to square root. \n

**Newton-Raphson Method**\n
Let **n** be the number you are attempting to square root, **x** be your first guess, and **y** be your solution. \n
y = x - (x^2 - n) / (2 * x)

"""

CONVERSIONS_MD = """\
Each **unit conversion** allows for a range of correct solutions. \
You must answer within 1% of the interval defined by the exact solution and the mental approximation. \
The upper bound and lower bounds are rounded up and down to the nearest integer, respectively. \n

| Conversion               | Exact Formula                 | Approximate Formula                             |
|--------------------------|-------------------------------|---------------------------------------------|
| Pounds -> Kilograms       | kg = 0.4535924 × lb           | kg = 0.45 × lb; or lb ÷ 2 − 10%             |
| Kilograms -> Pounds       | lb = 2.204623 × kg            | lb = 2.2 × kg; or kg × 2 + 10%              |
| Miles -> Kilometers       | km = 0.6213712 × mi           | km = 0.625 × mi; or mi ÷ 8 × 5              |
| Kilometers -> Miles       | mi = 1.609344 × km            | mi = 1.6 × km; or km × 8 ÷ 5                |
| Celsius -> Fahrenheit     | F = C × 1.8 + 32              | F = C × 2 + 30                              |
| Fahrenheit -> Celsius     | C = (F − 32) ÷ 1.8            | C = (F − 30) ÷ 2                            |

"""


SPECIAL_MD = """\
Selecting **special** from the menu screen takes you to the specials screen. \n
**Times tables** allows you to enter a specific number and practice its times table. \
Choose the number you want to practice, and the value you want to practice up to. \n
**Default** is three digit addition and subtraction and two digit multiplication, squaring, and square roots. \n
**Calendar** gives you a date between the years 1600-2099, as per the rules in the Memoriad or the Mental Calculation World Cup. \
Your answer is the day of the week that that day was.

| Day           | Accepted Inputs (not case sensitive) |
| ------------- | ---------------------------          |
| **Sunday**    | sunday, sun, 0                       |
| **Monday**    | monday, mon, m, 1                       |
| **Tuesday**   | tuesday, tue, tues, t, 2                |
| **Wednesday** | wednesday, wed, w, 3                    |
| **Thursday**  | thursday, thu, th, thurs, 4          |
| **Friday**    | friday, fri, f, 5                       |
| **Saturday**  | saturday, sat, 6                     |
"""


class Content(VerticalScroll, can_focus=False): ...


class HelpScreen(ModalScreen):
    CSS_PATH = "styles/help_screen.tcss"
    BINDINGS = [("escape", "close", "Close")]

    def compose(self) -> ComposeResult:
        with Content():
            yield Markdown(MMATH_MAIN_MD)
            with Collapsible(title="Get Started", collapsed=False):
                yield Markdown(GET_STARTED_MD)
            with Collapsible(title="Settings"):
                yield Markdown(TIMER_VANISH_MD)
            with Collapsible(title="Arithmetic"):
                yield Markdown(ARITHMETIC_MD)
            with Collapsible(title="Division"):
                yield Markdown(DIVISION_MD)
            with Collapsible(title="Fractions"):
                yield Markdown(FRACTIONS_MD)
            with Collapsible(title="Complex"):
                yield Markdown(COMPLEX_MD)
            with Collapsible(title="Square Root"):
                yield Markdown(SQUARE_ROOT_MD)
            with Collapsible(title="Unit Conversions"):
                yield Markdown(CONVERSIONS_MD)
            with Collapsible(title="Special"):
                yield Markdown(SPECIAL_MD)
        yield Footer()

    def action_close(self) -> None:
        self.app.pop_screen()
