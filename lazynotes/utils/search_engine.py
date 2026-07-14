"""Búsqueda difusa por título/contenido y filtrado exacto por #tags."""

from __future__ import annotations

from rapidfuzz import fuzz, process

from lazynotes.models.note import Note

FUZZY_SCORE_CUTOFF = 40


def fuzzy_search(notes: list[Note], query: str) -> list[tuple[Note, float]]:
    """Devuelve las notas que hacen fuzzy-match con `query` en título o contenido, ordenadas por score."""
    query = query.strip()
    if not query:
        return [(note, 100.0) for note in notes]

    scored: list[tuple[Note, float]] = []
    for note in notes:
        haystack = f"{note.title} {note.content}"
        score = fuzz.partial_ratio(query.lower(), haystack.lower())
        if score >= FUZZY_SCORE_CUTOFF:
            scored.append((note, score))

    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored


def filter_by_tag(notes: list[Note], tag: str) -> list[Note]:
    """Devuelve todas las notas cuya lista de tags contenga `tag`, sin importar la carpeta."""
    tag = tag.lstrip("#").strip().lower()
    return [note for note in notes if tag in (t.lstrip("#").lower() for t in note.tags)]


def all_tags(notes: list[Note]) -> list[str]:
    """Lista única y ordenada de todos los tags presentes en el set de notas."""
    tags = {t.lstrip("#") for note in notes for t in note.tags}
    return sorted(tags)
