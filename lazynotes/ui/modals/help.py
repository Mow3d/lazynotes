"""Help modal (key '?'): renders docs/KEYBINDINGS.md as the single source of truth."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Markdown

from lazynotes.config import PROJECT_ROOT

KEYBINDINGS_DOC = PROJECT_ROOT / "docs" / "KEYBINDINGS.md"


class HelpModal(ModalScreen[None]):
    DEFAULT_CSS = """
    HelpModal {
        align: center middle;
    }
    #help_box {
        width: 90%;
        height: 90%;
        border: round $accent;
        background: $panel;
        padding: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        if KEYBINDINGS_DOC.exists():
            text = KEYBINDINGS_DOC.read_text(encoding="utf-8")
        else:
            text = "# Keybindings\n\nDocument not found."
        with VerticalScroll(id="help_box"):
            yield Markdown(text)

    def on_key(self, event) -> None:
        if event.key in ("escape", "question_mark"):
            self.dismiss(None)
