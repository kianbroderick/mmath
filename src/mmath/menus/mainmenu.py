from typing import TYPE_CHECKING

from textual import on
from textual.containers import Center, Container, Vertical
from textual.events import Key
from textual.validation import Number
from textual.widget import Widget
from textual.widgets import (
    Button,
    Input,
    SelectionList,
)
from textual.widgets.selection_list import Selection

from mmath.config import CONFIG
from mmath.special.special_screen import SelectSpecialScreen

if TYPE_CHECKING:
    from textual.app import ComposeResult


class SelectOperations(Vertical):
    def compose(self) -> ComposeResult:
        self.selection_list = SelectionList(
            *(
                Selection(op.replace("_", " ").lower(), op, id=op)
                for op in CONFIG.QUESTIONDATA
            )
        )
        yield self.selection_list

    @on(Key)
    def vim_bindings(self, event: Key) -> None:
        if event.key == "j":
            self.selection_list.action_cursor_down()
        elif event.key == "k":
            self.selection_list.action_cursor_up()


class MainMenu(Widget):
    BINDINGS = [
        ("s", "special_screen", "Special"),
    ]

    DEFAULT_CSS = """
    SelectOperations {
        margin: 3;
        padding: 2 3;
        max-width: 60;
    }
    MainMenu {
        Button {
            margin: 0;
            padding: 0 0;
        }
        Input {
            max-width: 80;
        }
    }
    """

    def compose(self) -> ComposeResult:
        self.ops = SelectOperations()
        self.special_button = Button("Special", id="go_to_specials")
        self.input_numq = Input(
            type="integer",
            placeholder="How many questions?",
            validators=[Number(minimum=1)],
            valid_empty=False,
            validate_on=("changed",),
            id="input_number_of_questions",
        )
        self.next_button = Button(
            "Next", disabled=True, id="next_button_to_maxes", classes="next_button"
        )
        yield Center(self.ops)
        yield Center(self.special_button)
        yield Center(self.input_numq, self.next_button, id="input_numq_row")

    def _update_button_state(self) -> None:
        has_selection = bool(self.ops.selection_list.selected)
        has_num_q = bool(self.input_numq.value)
        self.next_button.disabled = not (
            has_selection and has_num_q and self.input_numq.is_valid
        )

    def on_selection_list_selected_changed(self) -> None:
        self._update_button_state()

    def on_input_changed(self) -> None:
        self._update_button_state()

    def action_special_screen(self) -> None:
        self.app.push_screen(SelectSpecialScreen())
