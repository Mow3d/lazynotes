"""Read-only widget: renders a note as Markdown."""

from __future__ import annotations

from textual.widgets import Markdown

from lazynotes.models.note import Note


class NoteViewer(Markdown):
    DEFAULT_CSS = """
    NoteViewer {
        border: round $accent;
        padding: 0 1;
    }
    """

    def on_mount(self) -> None:
        self.border_title = "NOTE VIEWER / EDITOR"

    def show_note(self, note: Note) -> None:
        header = (
            f"**Title:** {note.title}\n\n"
            f"**Tags:** {', '.join(f'#{t}' for t in note.tags) or '—'}\n\n"
            f"**Color:** `{note.color}`  ·  **Modified:** {note.modified or note.created}\n\n"
            "---\n\n"
        )
        self.update(header + note.content)

    def show_placeholder(self) -> None:
        self.update("# Select a note\n\nUse `j`/`k` to navigate and `Enter` to open it.")
