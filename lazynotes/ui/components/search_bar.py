"""Telescope-style fuzzy search bar, with #tag filtering support."""

from __future__ import annotations

from textual.widgets import Input


class SearchBar(Input):
    DEFAULT_CSS = """
    SearchBar {
        border: round $accent;
        height: 3;
    }
    """

    def __init__(self) -> None:
        super().__init__(placeholder="Search notes... ( / to focus, #tag to filter by tag)")

    def on_mount(self) -> None:
        self.border_title = "SEARCH"
