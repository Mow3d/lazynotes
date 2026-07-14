"""Bottom status bar: app name, date/time, active note path and mode."""

from __future__ import annotations

from datetime import datetime

from textual.reactive import reactive
from textual.widgets import Static


class StatusBar(Static):
    note_path: reactive[str] = reactive("no note selected")
    mode: reactive[str] = reactive("read")

    def on_mount(self) -> None:
        self.set_interval(30, self._refresh)
        self._refresh()

    def _refresh(self) -> None:
        now = datetime.now()
        today = now.strftime("%d %b")
        clock = now.strftime("%I:%M %p")
        self.update(
            f" 📝 LazyNotes  │  {self.mode}  │  📅 {today}  │  {clock}  │  {self.note_path}"
        )

    def watch_note_path(self, _old: str, _new: str) -> None:
        self._refresh()

    def watch_mode(self, _old: str, _new: str) -> None:
        self._refresh()
