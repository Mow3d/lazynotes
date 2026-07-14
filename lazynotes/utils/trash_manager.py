"""Gestión de papelera: soft-delete y purga automática de notas >30 días."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from lazynotes.config import TRASH_DIR, TRASH_RETENTION_DAYS
from lazynotes.models.note import Note


def move_to_trash(note: Note) -> Note:
    """Mueve el archivo de la nota a Trash/ y marca deleted_at con la fecha de hoy."""
    TRASH_DIR.mkdir(parents=True, exist_ok=True)
    destination = TRASH_DIR / note.path.name
    counter = 1
    while destination.exists():
        destination = TRASH_DIR / f"{note.path.stem}-{counter}{note.path.suffix}"
        counter += 1

    note.deleted_at = str(date.today())
    note.save()
    note.path.rename(destination)
    note.path = destination
    return note


def purge_expired_trash(today: date | None = None) -> list[Path]:
    """Elimina físicamente del disco las notas de Trash/ con más de TRASH_RETENTION_DAYS días.

    Se ejecuta al arrancar la aplicación. Devuelve las rutas purgadas.
    """
    today = today or date.today()
    purged: list[Path] = []

    if not TRASH_DIR.exists():
        return purged

    for md_path in TRASH_DIR.glob("*.md"):
        note = Note.load(md_path)
        deleted_at = note.deleted_at
        if deleted_at:
            deleted_date = datetime.strptime(deleted_at, "%Y-%m-%d").date()
        else:
            deleted_date = date.fromtimestamp(md_path.stat().st_mtime)

        if (today - deleted_date).days > TRASH_RETENTION_DAYS:
            md_path.unlink()
            purged.append(md_path)

    return purged
