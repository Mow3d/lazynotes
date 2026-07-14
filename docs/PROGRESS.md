# 📊 LazyNotes — Historial de Desarrollo y Estado del Proyecto

## 1. Concepto y Visión
Crear una aplicación de notas para el terminal de Linux inspirada en LazyVim y LazyGit. La UI toma como modelo exacto la maqueta `Gemini_Generated_Image_jecjemjecjemjecj.png`.

---

## 2. Decisiones de Diseño Tomadas (Log de Decisiones)
* **[2026-07-14] Stack Principal:** Se seleccionó **Python + Textual** por su alta compatibilidad con terminales modernas en Linux, facilidad de diseño CSS y soporte maduro de widgets.
* **[2026-07-14] Edición Interna:** Se acordó utilizar el widget embebido `TextArea` dentro de un `ContentSwitcher` en lugar de invocar un `$EDITOR` externo.
* **[2026-07-14] Selección de Colores:** Los colores asignados a las notas se eligen con un modal flotante (`c`) y se persisten en el YAML Frontmatter bajo la clave `color:`.
* **[2026-07-14] Filtrado Transversal por Tags:** Los tags no dependen de las carpetas físicas; el buscador compilará dinámicamente cualquier nota con el tag seleccionado.
* **[2026-07-14] Papelera y Auto-Cleanup:** Se implementa Soft Delete hacia `notes/Trash/` con un ciclo de vida automático de 30 días antes del borrado definitivo.
* **[2026-07-14] Alcance V1:** Aplicación 100% local sin integración con Git ni servicios cloud en la primera etapa.
* **[2026-07-14] Estructura Modular Adoptada:** Se migró el prototipo de un solo archivo (`codigo2.py`) a la estructura modular de `ARCHITECTURE_AND_ENGINEERING.md`. Regla clave: `models/` y `utils/` no importan `textual` (backend independiente de la UI, testeable sin levantar la TUI) — analogía directa con la separación frontend/backend que el usuario ya conoce de desarrollo web.
* **[2026-07-14] Colores de libre asignación:** La tabla color↔categoría del modal (`c`) es solo una sugerencia visual; el usuario asigna cualquier color a cualquier nota sin restricciones.
* **[2026-07-14] Layout confirmado por mockup del usuario:** Búsqueda arriba-izquierda, explorador abajo-izquierda, visor/editor a la derecha ocupando toda la altura, barra de estado abajo. El indicador `main*` estilo Git en la barra de estado es puramente decorativo (no hay integración real con Git en Fase 1).
* **[2026-07-14] Código legacy preservado:** `codigo1.py` y `codigo2.py` (prototipos originales del usuario) no se borraron; se archivaron en `legacy/` como referencia histórica.

---

## 3. Estado Actual del Desarrollo
* [x] Definición conceptual y maquetación visual.
* [x] Selección del stack tecnológico (Python / Textual / Rich / Frontmatter / RapidFuzz).
* [x] Prototipo funcional básico (MVP) en un solo archivo probando el `ContentSwitcher` y el modal de color (`legacy/codigo2.py`).
* [x] Definición completa de la documentación de arquitectura, requerimientos y progreso.
* [x] Estructura modular de carpetas (`docs/`, `lazynotes/{models,ui,utils}`, `notes/{Personal,Work,Archive,Trash}`, `legacy/`).
* [x] Entorno virtual (`.venv`) con `textual`, `rich`, `python-frontmatter`, `rapidfuzz` instalados y fijados en `requirements.txt` / `pyproject.toml`.
* [x] Backend completo: `config.py`, `models/note.py`, `utils/file_manager.py`, `utils/trash_manager.py`, `utils/search_engine.py`.
* [x] UI completa: `explorer.py`, `viewer.py`, `editor.py`, `search_bar.py`, `status_bar.py`, `modals/color_picker.py`, `modals/new_note.py`, `modals/help.py`.
* [x] `app.py` ensamblado, corrigiendo bugs detectados en el prototipo original (ver bitácora).
* [x] Smoke test automatizado (Textual `Pilot`, headless) validando el flujo completo: abrir nota → editar → guardar → cambiar color → buscar → crear nota → borrar (Trash) → ayuda.
* [x] Prueba interactiva confirmada por el usuario en terminal real (`.venv/bin/python -m lazynotes.app`).
* [x] Paneles nombrados (`SEARCH`, `NOTES EXPLORER`, `NOTE VIEWER / EDITOR`) usando `border_title` nativo de Textual, siguiendo `docs/mockup.png` provisto por el usuario.
* [x] Interfaz de la app traducida completamente a inglés (textos de UI, notificaciones, `docs/KEYBINDINGS.md`). La documentación de proceso (`REQUIREMENTS`, `ARCHITECTURE`, `PROGRESS`/bitácora) se mantiene en español.
* [x] Confirmado por el usuario: el explorador con texto coloreado + icono ya es suficiente, sin agregar un punto de color extra (evitar sobrecarga visual) — decisión de diseño minimalista guardada en memoria de largo plazo.
* [x] Corregido: al entrar en modo edición, el cursor aparecía en la posición (0,0), arriba a la izquierda, arriesgando que cualquier tecleo dañara el encabezado `# Título` de la nota. Ahora el cursor se posiciona al final del contenido (`TextArea.move_cursor(document.end)`).
* [x] Cambio de UX: crear una nota nueva (`n`) ahora entra directo en modo edición (antes quedaba en el visor, requiriendo presionar `e` a mano).
* [x] Bug encontrado y corregido durante la verificación: sin foco explícito, Textual podía dejar el foco en `SearchBar` (p. ej. al arrancar la app, o tras cancelar una edición con `Esc`), haciendo que atajos globales de una sola tecla (`e`, `c`, `d`, `n`) se escribieran como texto literal en la barra de búsqueda en vez de disparar la acción. Se fuerza foco explícito en `NotesExplorer` al arrancar y al cancelar edición.
* [x] Repositorio subido a GitHub: `https://github.com/Mow3d/lazynotes.git` (público, rama `main`). Commit inicial con todo el proyecto. `origin` configurado sin credenciales guardadas — la próxima sesión que necesite hacer push va a requerir autenticación nueva.
* [ ] **Siguiente hito:** Seguir puliendo el layout visual (porcentajes de scroll en los títulos de borde, indicador de rama tipo Git decorativo, colores por categoría) — pendiente de feedback del usuario, se van tratando de a un ajuste por vez.

---

## 4. Bitácora de Sesiones de Trabajo

### Sesión 2026-07-14
* Se revisaron los 3 documentos base y se confirmó comprensión del alcance (US-01 a US-05).
* El usuario mostró un mockup ASCII del layout y del modal de color, y aclaró que la asignación de color es libre (la tabla color↔categoría es solo sugerencia).
* El usuario compartió código previo (`codigo1.py`, `codigo2.py`) y `KEYBINDINGS.md`. Revisión encontró:
  * `codigo2.py` ya resolvía carga/guardado de notas con frontmatter y el patrón `ContentSwitcher` (viewer/editor) — se usó como base funcional.
  * Bugs detectados y corregidos en la migración: binding `n` sin `action_new_note` implementado; color `"orange"` no es un nombre válido de Rich/Textual (se reemplazó por `"dark_orange"` en la paleta); reconstrucción incorrecta de `DirectoryTree.FileSelected` con un `str` en vez de `Path`; sin lógica de papelera ni búsqueda fuzzy real pese a estar en los bindings.
* Se creó la estructura modular completa y se migró/extendió la lógica a `lazynotes/{models,utils,ui}`.
* Bug nuevo encontrado y corregido durante el desarrollo: `python-frontmatter` (1.3.0) usa `CSafeDumper` (libyaml, versión en C) por defecto, que escapa emojis fuera del BMP (`icon: "\U0001F4C4"`) pese a `allow_unicode=True`. Se fuerza `Dumper=yaml.SafeDumper` (puro Python) en `Note.save()` para guardar los emojis de forma legible.
* Bug nuevo encontrado y corregido: el slug de `new_note_path()` no sanitizaba caracteres como `:` o `/` en el título, generando rutas de archivo inválidas (ej. creaba subcarpetas por error). Se agregó una regex de sanitización.
* Se validó todo el flujo end-to-end con un smoke test headless (`Pilot`) y se generaron 5 notas de ejemplo en `notes/` (Personal, Work, Archive) para pruebas manuales.
* No había `tmux` instalado (ni sudo sin contraseña) para el patrón estándar de captura de TUIs vía agente; se usó en su lugar `App.export_screenshot()` de Textual (headless) para generar capturas SVG con los colores reales y mostrarlas en un Artifact.
* El usuario confirmó que corrió la app interactivamente en una terminal real y que se ve bien.
* El usuario compartió `docs/mockup.png` (imagen de referencia más detallada que el ASCII inicial) y pidió, para esta iteración puntual: (1) paneles visualmente divididos y nombrados — `SEARCH`, `NOTES EXPLORER`, `NOTE VIEWER / EDITOR` — y (2) traducir toda la interfaz de la app a inglés.
* Implementado usando `border_title` nativo de Textual (no requiere dibujar separadores a mano): cada widget (`SearchBar`, `NotesExplorer`, `NoteViewer`, `NoteEditor`) declara su propio borde + título en su propio `DEFAULT_CSS`, en vez de un borde compartido a nivel de panel — mantiene la separación modular ya establecida.
* Se tradujo a inglés: todos los textos de `app.py` (bindings, notificaciones, modo lectura/edición), todos los componentes UI, todos los modales, y `docs/KEYBINDINGS.md` (porque se muestra en vivo dentro de la app vía `?`). Los demás documentos de `/docs` (requerimientos, arquitectura, esta bitácora) se mantienen en español a propósito, ya que son para contexto de desarrollo, no parte de la app en sí.
* Notas de ejemplo regeneradas con contenido en inglés para consistencia visual.
* El usuario probó la app en terminal real, confirmó que el árbol se ve bien tal como está (texto coloreado + icono, sin punto extra), y reportó dos observaciones de UX sobre el editor, ambas corregidas y verificadas con tests automatizados en esta misma sesión (ver checklist arriba: cursor al final del contenido, nota nueva entra directo en edición, fix de foco).
* Considerar correr `/run-skill-generator` para capturar el método de captura de pantalla headless (Textual `export_screenshot`, ya que no hay `tmux` disponible en este entorno) como skill reutilizable del proyecto.
* **Repo subido a GitHub:** el usuario pidió subir todo a `https://github.com/Mow3d/lazynotes.git` (repo público, vacío al momento del push) y compartió un token de acceso personal temporal en el chat. Se inicializó git local (`main`, identidad de commit `Mow3d` / `mowgly@gmail.com` — a confirmar/ajustar si no es lo que el usuario quiere), se hizo un commit inicial con los 35 archivos del proyecto (código, docs, notas de ejemplo, `legacy/`, sin `.venv/` ni `__pycache__`) y se pusheó. El token se usó solo como argumento puntual del `git push` (no quedó guardado en `.git/config` ni en ningún archivo — `origin` quedó con la URL limpia sin credenciales). **Para el próximo push**, el usuario va a necesitar autenticarse de nuevo (token nuevo, SSH key, o `gh auth login`), ya que no se guardó ninguna credencial persistente a propósito.
* Nota de seguridad/producto pendiente de decisión del usuario: el repo es público y por ahora incluye las notas de ejemplo (contenido genérico, no sensible) dentro de `notes/`. Cuando el usuario empiece a usar la app con notas personales reales, conviene decidir si `notes/` debe dejar de versionarse (agregarlo a `.gitignore`) para no exponer contenido personal en un repo público — todavía no se tomó esa decisión, solo se dejó anotada.
* **Cierre de sesión:** el usuario se retira y vuelve en otra sesión. Todo quedó commiteado, pusheado a GitHub y documentado (ver "Próximos pasos" abajo para retomar). No hay cambios a medio hacer ni archivos en estado roto — el repo está en un punto estable: smoke test pasa, notas de ejemplo limpias en `notes/`, `__pycache__` limpiado, working tree limpio (`git status` sin cambios pendientes al cierre).

---

## 5. Próximos Pasos (Backlog)

**Para arrancar la próxima sesión:** preguntarle al usuario qué observación sigue de probar la app (dijo que iba a seguir probando). Puede haber feedback nuevo antes de tocar lo de abajo.

1. Pulir el CSS de Textual para acercar la estética al mockup original (paleta de fondo, resaltado del ítem seleccionado en el explorador, porcentajes de scroll en los títulos de borde, rama Git decorativa en la barra de estado) — el usuario pidió ir de a un ajuste visual por vez, no aplicar todo junto.
2. Agregar tests formales con `pytest` para `models/note.py`, `utils/trash_manager.py` y `utils/search_engine.py` (hoy solo hay smoke tests manuales vía Textual `Pilot`, no versionados como suite de tests).
3. Revisar UX del modal `NewNoteModal`: hoy la categoría de la nota nueva se infiere de la nota actualmente seleccionada (o "Personal" por defecto); evaluar si conviene elegir categoría explícitamente.
4. Considerar inicializar Git en el repo del proyecto (control de versiones del código fuente) — distinto de la decisión de "sin Git" para el almacenamiento de notas en Fase 1. Ya existe `.gitignore` listo para cuando se decida.