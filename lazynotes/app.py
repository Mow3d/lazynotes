"""Entry point: assembles the components and defines the global actions."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import ContentSwitcher

from lazynotes.config import CATEGORIES, NOTES_DIR
from lazynotes.models.note import Note
from lazynotes.ui.components.editor import NoteEditor
from lazynotes.ui.components.explorer import NotesExplorer
from lazynotes.ui.components.search_bar import SearchBar
from lazynotes.ui.components.status_bar import StatusBar
from lazynotes.ui.components.viewer import NoteViewer
from lazynotes.ui.modals.color_picker import ColorPickerModal
from lazynotes.ui.modals.help import HelpModal
from lazynotes.ui.modals.new_note import NewNoteModal
from lazynotes.utils.file_manager import ensure_category_dirs, new_note_path, scan_notes
from lazynotes.utils.search_engine import fuzzy_search, filter_by_tag
from lazynotes.utils.trash_manager import move_to_trash, purge_expired_trash


class LazyNotesApp(App):
    CSS = """
    Screen {
        layout: vertical;
        background: $surface;
    }
    #main_container {
        layout: horizontal;
        height: 1fr;
    }
    #left_panel {
        width: 35%;
    }
    #right_panel {
        width: 65%;
    }
    ContentSwitcher {
        height: 1fr;
    }
    StatusBar {
        height: 1;
        background: $panel;
        dock: bottom;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("slash", "focus_search", "Search"),
        Binding("tab", "cycle_focus", "Switch panel", show=False),
        Binding("question_mark", "show_help", "Help"),
        Binding("n", "new_note", "New note"),
        Binding("c", "change_color", "Color"),
        Binding("d", "delete_note", "Delete"),
        Binding("e", "edit_note", "Edit"),
        Binding("escape", "cancel_edit", "Cancel", show=False),
        Binding("ctrl+s", "save_note", "Save", show=False),
    ]

    current_note: Note | None = None
    all_notes: list[Note] = []

    def compose(self) -> ComposeResult:
        with Container(id="main_container"):
            with Vertical(id="left_panel"):
                yield SearchBar()
                yield NotesExplorer()
            with Vertical(id="right_panel"):
                with ContentSwitcher(initial="viewer_view"):
                    yield NoteViewer(id="viewer_view")
                    yield NoteEditor(id="editor_view")
        yield StatusBar()

    def on_mount(self) -> None:
        ensure_category_dirs()
        purged = purge_expired_trash()
        if purged:
            self.notify(f"Purged {len(purged)} note(s) older than 30 days from Trash.")
        self.query_one(NoteViewer).show_placeholder()
        self.reload_notes()
        # Without an explicit focus target, Textual can default focus to the
        # SearchBar, which then swallows single-key shortcuts (e, c, d, n) as
        # literal typed text instead of triggering the matching action.
        self.query_one(NotesExplorer).focus()

    def reload_notes(self) -> None:
        self.all_notes = scan_notes()
        self.query_one(NotesExplorer).populate(self.all_notes)

    # --- Navigation and search --------------------------------------------------

    def action_focus_search(self) -> None:
        self.query_one(SearchBar).focus()

    def action_cycle_focus(self) -> None:
        if self.focused is self.query_one(NotesExplorer):
            self.query_one(ContentSwitcher).query_one(f"#{self.query_one(ContentSwitcher).current}").focus()
        else:
            self.query_one(NotesExplorer).focus()

    def on_input_submitted(self, event) -> None:
        if event.input.id != self.query_one(SearchBar).id and not isinstance(event.input, SearchBar):
            return
        query = event.value.strip()
        if query.startswith("#"):
            results = filter_by_tag(self.all_notes, query)
        else:
            results = [note for note, _score in fuzzy_search(self.all_notes, query)]
        self.query_one(NotesExplorer).populate(results)
        self.query_one(NotesExplorer).focus()

    def on_notes_explorer_note_selected(self, event: NotesExplorer.NoteSelected) -> None:
        self.load_note(event.note)

    def load_note(self, note: Note) -> None:
        self.current_note = note
        self.query_one(NoteViewer).show_note(note)
        self.query_one(ContentSwitcher).current = "viewer_view"
        self.query_one(StatusBar).note_path = str(note.path.relative_to(NOTES_DIR))
        self.query_one(StatusBar).mode = "read"

    # --- Editing -----------------------------------------------------------

    def action_edit_note(self) -> None:
        if not self.current_note:
            self.notify("Select a note first.", severity="warning")
            return
        self.query_one(NoteEditor).load_content(self.current_note.content)
        self.query_one(ContentSwitcher).current = "editor_view"
        self.query_one(NoteEditor).focus()
        self.query_one(StatusBar).mode = "edit"

    def action_save_note(self) -> None:
        if not self.current_note or self.query_one(ContentSwitcher).current != "editor_view":
            return
        self.current_note.content = self.query_one(NoteEditor).text
        self.current_note.save()
        self.load_note(self.current_note)
        self.notify("Note saved.")

    def action_cancel_edit(self) -> None:
        if self.query_one(ContentSwitcher).current == "editor_view":
            self.query_one(ContentSwitcher).current = "viewer_view"
            self.query_one(StatusBar).mode = "read"
            self.query_one(NotesExplorer).focus()

    # --- Color ---------------------------------------------------------------

    def action_change_color(self) -> None:
        if not self.current_note:
            self.notify("Select a note first.", severity="warning")
            return

        def apply_color(color: str | None) -> None:
            if color and self.current_note:
                self.current_note.color = color
                self.current_note.save()
                self.reload_notes()
                self.load_note(self.current_note)
                self.notify(f"Color updated to {color}.")

        self.push_screen(ColorPickerModal(), apply_color)

    # --- New note / Delete --------------------------------------------------

    def action_new_note(self) -> None:
        def create(title: str | None) -> None:
            if not title:
                return
            category_name = self.current_note.path.parent.name if self.current_note else CATEGORIES["1"]
            category_dir = NOTES_DIR / category_name
            path = new_note_path(category_dir, title)
            note = Note.create(path, title, category_dir)
            self.reload_notes()
            self.load_note(note)
            self.action_edit_note()  # a new note goes straight into edit mode, ready to write
            self.notify(f"Note created in {category_name}/")

        self.push_screen(NewNoteModal(), create)

    def action_delete_note(self) -> None:
        if not self.current_note:
            self.notify("Select a note first.", severity="warning")
            return
        move_to_trash(self.current_note)
        self.notify("Note moved to Trash/.")
        self.current_note = None
        self.query_one(NoteViewer).show_placeholder()
        self.query_one(StatusBar).note_path = "no note selected"
        self.reload_notes()

    # --- Help -----------------------------------------------------------------

    def action_show_help(self) -> None:
        self.push_screen(HelpModal())


def run() -> None:
    LazyNotesApp().run()


if __name__ == "__main__":
    run()
