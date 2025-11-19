from typing import TYPE_CHECKING

from textual.containers import Vertical
from textual.validation import Number
from textual.widget import Widget
from textual.widgets import (
    Button,
    Input,
    SelectionList,
)
from textual.widgets.selection_list import Selection

from mmath.config import CONFIG

if TYPE_CHECKING:
    from textual.app import ComposeResult


class SelectOperations(Vertical):
    def compose(self) -> ComposeResult:
        self.selection_list = SelectionList(
            *(Selection(op, op, id=op) for op in CONFIG.OPERATIONS)
        )
        yield self.selection_list


class MainMenu(Widget):
    def compose(self) -> ComposeResult:
        self.ops = SelectOperations()
        self.special_button = Button("Special")
        self.input_numq = Input(
            type="integer",
            placeholder="How many questions?",
            validators=[Number(minimum=1)],
            valid_empty=False,
            validate_on=("changed",),
        )
        self.next_button = Button("Next", disabled=True, id="next_button_to_maxes")
        yield self.ops
        yield self.special_button
        yield self.input_numq
        yield self.next_button

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
