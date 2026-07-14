"""Modelo de Nota: mapeo entre un archivo .md con YAML Frontmatter y un objeto Python."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import frontmatter
import yaml

from lazynotes.config import DEFAULT_COLOR


@dataclass
class Note:
    path: Path
    title: str = "Sin título"
    tags: list[str] = field(default_factory=list)
    created: str = ""
    modified: str = ""
    deleted_at: str | None = None
    color: str = DEFAULT_COLOR
    icon: str = "📄"
    content: str = ""

    @classmethod
    def load(cls, path: Path) -> "Note":
        post = frontmatter.load(path)
        return cls(
            path=path,
            title=post.get("title", path.stem),
            tags=list(post.get("tags", [])),
            created=post.get("created", ""),
            modified=post.get("modified", ""),
            deleted_at=post.get("deleted_at"),
            color=post.get("color", DEFAULT_COLOR),
            icon=post.get("icon", "📄"),
            content=post.content,
        )

    def save(self) -> None:
        """Escribe la nota a disco actualizando `modified` a hoy."""
        self.modified = str(date.today())
        post = frontmatter.Post(self.content)
        post["title"] = self.title
        post["tags"] = self.tags
        post["created"] = self.created or self.modified
        post["modified"] = self.modified
        post["deleted_at"] = self.deleted_at
        post["color"] = self.color
        post["icon"] = self.icon
        with open(self.path, "w", encoding="utf-8") as f:
            # Dumper=yaml.SafeDumper evita un bug del dumper en C (libyaml) que
            # escapa emojis fuera del BMP (p.ej. "\U0001F4C4") pese a allow_unicode=True.
            frontmatter.dump(post, f, Dumper=yaml.SafeDumper)

    @classmethod
    def create(cls, path: Path, title: str, category_dir: Path) -> "Note":
        """Crea una nota nueva vacía en `category_dir` y la guarda en disco."""
        today = str(date.today())
        note = cls(
            path=path,
            title=title,
            tags=[],
            created=today,
            modified=today,
            deleted_at=None,
            color=DEFAULT_COLOR,
            icon="📄",
            content=f"# {title}\n\n",
        )
        category_dir.mkdir(parents=True, exist_ok=True)
        note.save()
        return note
