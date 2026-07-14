# 📌 LazyNotes — Requerimientos y Historias de Usuario

## 1. Descripción General del Producto
LazyNotes es una aplicación TUI (Text User Interface) ligera, minimalista y ultra rápida diseñada para ejecutarse exclusivamente en el terminal de Linux. Inspirada en la filosofía de uso por teclado de aplicaciones como LazyVim y LazyGit, su objetivo es permitir la creación, organización, lectura, edición y búsqueda difusa de notas en formato Markdown local con metadatos estructurados.

La interfaz toma como referencia el diseño visual de `Gemini_Generated_Image_jecjemjecjemjecj.png`, ofreciendo un layout divido en cuadrantes, explorador con codificación de colores por nota, visor de Markdown con sintaxis enriquecida, editor integrado y una barra de estado inferior.

---

## 2. Requerimientos Funcionales Core
1. **Navegación TUI por Teclado:** Uso completo de teclas estilo Vim (`j`, `k`, `h`, `l`, `Tab`, `Enter`, `Esc`).
2. **Explorador de Notas y Carpetas:**
   * Árbol de directorios con iconos Nerd Fonts.
   * Identificación visual de cada nota mediante un distintivo cromático (Color Badge).
   * Teclas de acceso directo a categorías (`[1]`, `[2]`, `[3]`).
3. **Búsqueda Difusa y Filtrado Dinámico por Etiquetas:**
   * Barra superior estilo *Telescope* para filtrar por título, fecha o texto interno.
   * Filtrado dinámico por `#tags`: Al seleccionar o buscar un tag, se mostrarán todas las notas coincidentes independientemente de la carpeta física donde se encuentren almacenadas.
4. **Visor y Editor Integrado:**
   * **Modo Lectura:** Renderizado fluido de Markdown (negritas, listas, bloques de código, encabezados).
   * **Modo Edición:** Editor de texto plano embebido (`TextArea`) accesible con la tecla `e` y guardado mediante `Ctrl+S`.
5. **Asignación Interactiva de Colores:**
   * Modal flotante activado por la tecla `c` para elegir el color de la nota actual (Amarillo, Azul, Morado, Verde, Naranja, Rojo, Gris).
6. **Gestión de Papelera de Reciclaje (Soft Delete):**
   * Al presionar `d`, la nota no se borra definitivamente, sino que se mueve a la carpeta `Trash/`.
   * Las notas en `Trash/` que superen los 30 días de antigüedad desde la fecha de eliminación se purgarán automáticamente.
7. **Persistencia Local:**
   * Sin dependencias de red ni Git en la Fase 1. Manejo 100% local en archivos `.md` con YAML Frontmatter.

---

## 3. Historias de Usuario (User Stories)

### US-01: Navegación de Notas por Teclado
* **Como:** Usuario de Linux enfocado en la productividad.
* **Quiero:** Navegar entre el árbol de notas y el panel principal usando atajos de teclado.
* **Para:** Moverme rápidamente sin necesidad de utilizar el ratón.

### US-02: Búsqueda y Filtrado Dinámico por Tags
* **Como:** Usuario que organiza contenidos por temáticas.
* **Quiero:** Filtrar notas por etiquetas (ej. `#proyecto`, `#idea`) y ver los resultados agrupados.
* **Para:** Encontrar información relacionada sin importar en qué subcarpeta esté guardada la nota.

### US-03: Edición Embebida sin Salir de la TUI
* **Como:** Creador de contenido y desarrollador.
* **Quiero:** Presionar `e` sobre una nota para editarla directamente en un editor interno.
* **Para:** Mantener una experiencia fluida sin saltos de contexto ni abrir editores externos.

### US-04: Codificación Visual mediante Paleta de Colores
* **Como:** Usuario visual que organiza sus tareas por colores.
* **Quiero:** Presionar `c` para desplegar un menú con colores predefinidos y asignarlo a una nota.
* **Para:** Identificar la categoría o prioridad de cada nota en el árbol de exploración.

### US-05: Papelera de Reciclaje con Retención de 30 Días
* **Como:** Usuario propenso a borrar archivos por error.
* **Quiero:** Mover notas eliminadas a una carpeta `Trash/` al presionar `d` y que se eliminen solas tras 30 días.
* **Para:** Recuperar notas borradas accidentalmente sin acumular basura indefinidamente.