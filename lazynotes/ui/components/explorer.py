"""Notes tree grouped by category, with a color badge per note."""

from __future__ import annotations

from rich.text import Text
from textual.binding import Binding
from textual.message import Message
from textual.widgets import Tree
from textual.widgets.tree import TreeNode

from lazynotes.config import CATEGORIES, COLOR_ICONS
from lazynotes.models.note import Note


class NotesExplorer(Tree):
    """Tree whose leaf nodes carry a Note in `.data`; category nodes carry None."""

    DEFAULT_CSS = """
    NotesExplorer {
        border: round $accent;
        height: 1fr;
    }
    """

    BINDINGS = [
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("l", "select_cursor", "Open", show=False),
        Binding("h", "cursor_parent", "Collapse", show=False),
        Binding("1", "jump_category('1')", "Personal", show=False),
        Binding("2", "jump_category('2')", "Work", show=False),
        Binding("3", "jump_category('3')", "Archive", show=False),
    ]

    class NoteSelected(Message):
        def __init__(self, note: Note) -> None:
            self.note = note
            super().__init__()

    def __init__(self) -> None:
        super().__init__("Notes")
        self.show_root = False
        self._category_nodes: dict[str, TreeNode] = {}

    def on_mount(self) -> None:
        self.border_title = "NOTES EXPLORER"
        for key, name in CATEGORIES.items():
            node = self.root.add(f"[{key}] 📁 {name}", data=None, expand=True)
            self._category_nodes[name] = node

    def populate(self, notes: list[Note]) -> None:
        """Clears and re-populates the tree from a list of notes."""
        for node in self._category_nodes.values():
            node.remove_children()

        fallback_name = list(CATEGORIES.values())[-1]
        for note in notes:
            category_name = note.path.parent.name
            node = self._category_nodes.get(category_name, self._category_nodes[fallback_name])
            icon = COLOR_ICONS.get(note.color, "📄")
            label = Text(f"{icon} {note.title}", style=note.color)
            node.add_leaf(label, data=note)

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        note = event.node.data
        if note is not None:
            event.stop()
            self.post_message(self.NoteSelected(note))

    def action_jump_category(self, key: str) -> None:
        name = CATEGORIES.get(key)
        node = self._category_nodes.get(name) if name else None
        if node is not None:
            self.select_node(node)
            self.scroll_to_node(node)
