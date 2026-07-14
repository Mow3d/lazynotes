"""Floating modal to assign a color to the current note (key 'c')."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Static

from lazynotes.config import COLOR_PALETTE


class ColorPickerModal(ModalScreen[str | None]):
    """Returns the chosen color name, or None if cancelled with Esc."""

    DEFAULT_CSS = """
    ColorPickerModal {
        align: center middle;
    }
    #color_picker_box {
        width: auto;
        height: auto;
        border: round $accent;
        background: $panel;
        padding: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="color_picker_box"):
            yield Static("[ Select a color for the note ]\n", id="modal_title")
            for key, (label, _) in COLOR_PALETTE.items():
                yield Static(f" [{key}] {label}")
            yield Static("\n Press the number, or Esc to cancel.")

    def on_key(self, event) -> None:
        if event.key in COLOR_PALETTE:
            self.dismiss(COLOR_PALETTE[event.key][1])
        elif event.key == "escape":
            self.dismiss(None)
