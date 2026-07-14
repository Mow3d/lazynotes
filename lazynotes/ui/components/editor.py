"""Embedded editing widget: TextArea over the note's Markdown content."""

from __future__ import annotations

from textual.widgets import TextArea


class NoteEditor(TextArea):
    DEFAULT_CSS = """
    NoteEditor {
        border: round $accent;
    }
    """

    def on_mount(self) -> None:
        self.border_title = "NOTE VIEWER / EDITOR"

    def load_content(self, content: str) -> None:
        self.text = content
        self.language = "markdown"
        # Cursor starts at the end, not (0, 0): editing an existing note
        # shouldn't land on top of its "# Title" heading line, and a brand
        # new note (content = "# Title\n\n") should be ready to type the body.
        self.move_cursor(self.document.end)
        self.scroll_cursor_visible()
