"""IO de notas: escaneo de notes/ y creación de notas nuevas."""

from __future__ import annotations

import re
from pathlib import Path

from lazynotes.config import NOTES_DIR, TRASH_DIR, CATEGORIES
from lazynotes.models.note import Note

_SLUG_INVALID_CHARS = re.compile(r"[^a-z0-9]+")


def ensure_category_dirs() -> None:
    """Crea las carpetas de categorías y Trash/ si no existen."""
    for name in CATEGORIES.values():
        (NOTES_DIR / name).mkdir(parents=True, exist_ok=True)
    TRASH_DIR.mkdir(parents=True, exist_ok=True)


def scan_notes(root: Path = NOTES_DIR) -> list[Note]:
    """Escanea recursivamente notes/ excluyendo Trash/ y devuelve las notas cargadas."""
    notes = []
    for md_path in sorted(root.rglob("*.md")):
        if TRASH_DIR in md_path.parents:
            continue
        notes.append(Note.load(md_path))
    return notes


def scan_trash() -> list[Note]:
    """Escanea las notas actualmente en Trash/."""
    if not TRASH_DIR.exists():
        return []
    return [Note.load(p) for p in sorted(TRASH_DIR.glob("*.md"))]


def new_note_path(category_dir: Path, title: str) -> Path:
    """Genera una ruta de archivo única a partir del título, evitando sobrescribir notas."""
    slug = _SLUG_INVALID_CHARS.sub("-", title.strip().lower()).strip("-") or "nota"
    candidate = category_dir / f"{slug}.md"
    counter = 1
    while candidate.exists():
        candidate = category_dir / f"{slug}-{counter}.md"
        counter += 1
    return candidate
