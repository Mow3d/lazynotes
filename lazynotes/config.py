"""Global constants: paths, color palette and categories."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = PROJECT_ROOT / "notes"
TRASH_DIR = NOTES_DIR / "Trash"

TRASH_RETENTION_DAYS = 30

# Categories with direct number-key access, in the order shown in the explorer.
CATEGORIES = {
    "1": "Personal",
    "2": "Work",
    "3": "Archive",
}

# Color name -> (visible label, color name valid for Rich/Textual).
# "orange" isn't a valid Rich color name; "dark_orange" is used instead.
COLOR_PALETTE = {
    "1": ("🟡 Yellow (Ideas)", "yellow"),
    "2": ("🔵 Blue (Journals)", "blue"),
    "3": ("🟣 Purple (Projects)", "magenta"),
    "4": ("🟢 Green (Personal)", "green"),
    "5": ("🟠 Orange (Meetings)", "dark_orange"),
    "6": ("🔴 Red (Priority)", "red"),
    "7": ("⚪ Gray (Default)", "grey66"),
}

DEFAULT_COLOR = "grey66"

# Icon shown in the explorer depending on the note's assigned color.
COLOR_ICONS = {
    "yellow": "📌",
    "blue": "📓",
    "magenta": "💡",
    "green": "🌿",
    "dark_orange": "📅",
    "red": "🔥",
    "grey66": "📄",
}
