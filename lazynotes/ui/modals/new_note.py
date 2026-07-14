"""Modal to create a new note (key 'n'): asks for the title."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Static


class NewNoteModal(ModalScreen[str | None]):
    """Returns the entered title, or None if cancelled with Esc."""

    DEFAULT_CSS = """
    NewNoteModal {
        align: center middle;
    }
    #new_note_box {
        width: 60;
        height: auto;
        border: round $accent;
        background: $panel;
        padding: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="new_note_box"):
            yield Static("[ New note — type the title ]\n")
            yield Input(placeholder="Note title...", id="new_note_input")
            yield Static("\nEnter to create · Esc to cancel")

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        title = event.value.strip()
        self.dismiss(title or None)

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.dismiss(None)
