# 🛠️ LazyNotes — Arquitectura e Ingeniería Técnica

## 1. Stack Tecnológico Definitivo
* **Entorno de Ejecución:** Linux (X11 / Wayland)
* **Lenguaje:** Python 3.10+
* **Framework TUI:** `textual` (UI, Layouts, Widgets, Eventos y Teclado)
* **Renderizado de Texto:** `rich` (Sintaxis Markdown y colores ANSI/TrueColor)
* **Gestión de Metadatos:** `python-frontmatter` (Lectura y escritura de encabezados YAML)
* **Motor de Búsqueda:** `rapidfuzz` (Búsqueda difusa de títulos, contenido y tags)

---

## 2. Estructura del Proyecto

lazynotes/
├── docs/                       # Documentación técnica para IAs y Devs
│   ├── REQUIREMENTS_AND_USER_STORIES.md
│   ├── ARCHITECTURE_AND_ENGINEERING.md
│   └── PROGRESS.md
├── lazynotes/                  # Código fuente principal
│   ├── __init__.py
│   ├── app.py                  # Entry point (Clase Principal Textual App)
│   ├── config.py               # Temas de color, rutas y constantes (ej. TRASH_RETENTION_DAYS = 30)
│   ├── models/
│   │   └── note.py             # Modelo de Nota (Mapeo entre Markdown y YAML)
│   ├── ui/
│   │   ├── components/
│   │   │   ├── explorer.py     # Widget del Árbol de Notas y Filtro por Tags
│   │   │   ├── viewer.py       # Widget Visor de Markdown
│   │   │   ├── editor.py       # Widget Editor TextArea
│   │   │   ├── search_bar.py   # Widget de búsqueda fuzzy
│   │   │   └── status_bar.py   # Barra de estado inferior local
│   │   └── modals/
│   │       └── color_picker.py # Modal emergente de paleta de colores
│   └── utils/
│       ├── file_manager.py     # IO para lectura, escritura y escaneo de subcarpetas
│       ├── trash_manager.py    # Gestión de papelera y purgado de archivos >30 días
│       └── search_engine.py    # Algoritmo RapidFuzz para filtrado por texto/tags
├── notes/                      # Directorio de almacenamiento de notas .md
│   └── Trash/                  # Directorio especial para notas eliminadas (Soft Delete)
├── requirements.txt
└── pyproject.toml

---

## 3. Modelo de Datos de Archivo (.md)
Cada nota almacenada en el disco local seguirá el formato YAML Frontmatter + Markdown estándar:

---
title: "Idea: LazyVim TUI Notes App"
tags: ["tui", "notes", "lazyvim"]
created: "2026-07-14"
modified: "2026-07-14"
deleted_at: null                 # Fecha en formato YYYY-MM-DD si está en Trash/
color: "yellow"
icon: "📌"
---

# Título de la Nota
Contenido en texto plano o Markdown...

---

## 4. Lógica de Componentes Especiales

### A. Filtro Dinámico por Tags
* Al presionar sobre un Tag o buscar `#tag_name`, `search_engine.py` escanea recursivamente todos los archivos en `notes/` (excluyendo `notes/Trash/`) y genera un árbol/vista virtual agrupando únicamente los archivos cuya lista `tags` contenga la coincidencia.

### B. Módulo de Purga de Papelera (`trash_manager.py`)
* Al arrancar la aplicación, `trash_manager.py` revisa todos los archivos dentro de `notes/Trash/`.
* Compara el metadato `deleted_at` (o la fecha de modificación del archivo) con la fecha actual del sistema.
* Si `días_transcurridos > 30`, el archivo se elimina físicamente del disco con `os.remove()`.