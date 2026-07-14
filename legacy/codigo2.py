import os
from datetime import date
import frontmatter
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, DirectoryTree, Markdown, TextArea, ContentSwitcher
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.binding import Binding

# --- MODAL DE PALETA DE COLORES (Tecla 'c') ---
class ColorPickerModal(ModalScreen[str]):
    COLORS = {
        "1": ("🟡 Amarillo (Ideas)", "yellow"),
        "2": ("🔵 Azul (Diarios)", "blue"),
        "3": ("🟣 Morado (Proyectos)", "magenta"),
        "4": ("🟢 Verde (Personal)", "green"),
        "5": ("🟠 Naranja (Reuniones)", "orange"),
        "6": ("🔴 Rojo (Prioridad)", "red"),
        "7": ("⚪ Gris (Por Defecto)", "gray"),
    }

    def compose(self) -> ComposeResult:
        yield Static("  [ SELECCIONAR COLOR PARA LA NOTA ]\n", id="modal_title")
        for key, (label, _) in self.COLORS.items():
            yield Static(f" [{key}] {label}")
        yield Static("\n Presiona el número del color o ESC para cancelar.")

    def on_key(self, event) -> None:
        if event.key in self.COLORS:
            self.dismiss(self.COLORS[event.key][1])
        elif event.key == "escape":
            self.dismiss(None)


# --- APLICACIÓN PRINCIPAL LAZYNOTES ---
class LazyNotesApp(App):
    CSS = """
    Screen {
        layout: vertical;
        background: #1e1e2e;
    }
    #main_container {
        layout: horizontal;
        height: 1fr;
    }
    #left_panel {
        width: 35%;
        border: solid #89b4fa;
        background: #181825;
    }
    #right_panel {
        width: 65%;
        border: solid #89b4fa;
        background: #1e1e2e;
        padding: 1 2;
    }
    #search_box {
        height: 3;
        border: double #f9e2af;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Salir"),
        Binding("e", "edit_note", "Editar"),
        Binding("ctrl+s", "save_note", "Guardar", show=False),
        Binding("c", "change_color", "Color"),
        Binding("n", "new_note", "Nueva Nota"),
        Binding("/", "focus_search", "Buscar"),
    ]

    current_file_path: str | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main_container"):
            with Vertical(id="left_panel"):
                yield Static("🔍 Buscar notas... [ / ]", id="search_box")
                yield DirectoryTree("./notes", id="notes_tree")
            
            with Vertical(id="right_panel"):
                # Alternador entre Visor (Markdown) y Editor (TextArea)
                with ContentSwitcher(initial="viewer_view"):
                    yield Markdown("# Selecciona una nota", id="viewer_view")
                    yield TextArea(id="editor_view")
                    
        yield Footer()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Carga el contenido y metadatos cuando el usuario selecciona un archivo."""
        self.current_file_path = str(event.path)
        if self.current_file_path.endswith(".md"):
            post = frontmatter.load(self.current_file_path)
            
            # Formatear vista previa en Markdown
            header_info = f"**Título:** {post.get('title', 'Sin Título')}\n"
            header_info += f"**Tags:** {', '.join(post.get('tags', []))}\n"
            header_info += f"**Color:** `{post.get('color', 'gray')}`\n"
            header_info += "---\n\n"
            
            full_content = header_info + post.content
            
            # Cargar en Visor y en Editor
            self.query_one("#viewer_view", Markdown).update(full_content)
            self.query_one("#editor_view", TextArea).text = post.content
            
            # Asegurar que estamos en modo lectura
            self.query_one(ContentSwitcher).current = "viewer_view"

    def action_edit_note(self) -> None:
        """Cambia al modo edición con TextArea."""
        if self.current_file_path:
            switcher = self.query_one(ContentSwitcher)
            switcher.current = "editor_view"
            self.query_one("#editor_view", TextArea).focus()
            self.notify("Modo Edición activo. Usa Ctrl+S para guardar.")

    def action_save_note(self) -> None:
        """Guarda el contenido editado actualizando el Frontmatter YAML."""
        if self.current_file_path and self.query_one(ContentSwitcher).current == "editor_view":
            new_text = self.query_one("#editor_view", TextArea).text
            
            post = frontmatter.load(self.current_file_path)
            post.content = new_text
            post["modified"] = str(date.today())
            
            with open(self.current_file_path, "wb") as f:
                frontmatter.dump(post, f)
            
            # Actualizar visor y volver a modo lectura
            self.on_directory_tree_file_selected(
                DirectoryTree.FileSelected(self.query_one("#notes_tree"), self.current_file_path)
            )
            self.notify("Nota guardada correctamente.")

    def action_change_color(self) -> None:
        """Modal de color."""
        if not self.current_file_path:
            self.notify("Selecciona una nota primero.", severity="warning")
            return

        def check_color(selected_color: str | None):
            if selected_color and self.current_file_path:
                post = frontmatter.load(self.current_file_path)
                post["color"] = selected_color
                with open(self.current_file_path, "wb") as f:
                    frontmatter.dump(post, f)
                self.notify(f"Color actualizado a: {selected_color}")

        self.push_screen(ColorPickerModal(), check_color)

if __name__ == "__main__":
    os.makedirs("./notes", exist_ok=True)
    app = LazyNotesApp()
    app.run()