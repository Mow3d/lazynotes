import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, DirectoryTree, Markdown
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.binding import Binding

# --- MODAL PARA SELECCIONAR COLOR (Tecla 'c') ---
class ColorPickerModal(ModalScreen[str]):
    """Ventana flotante para cambiar el color de la nota seleccionada."""
    
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
        yield Static("\n Presiona el número correspondiente o ESC para cancelar.")

    def on_key(self, event) -> None:
        if event.key in self.COLORS:
            color_name = self.COLORS[event.key][1]
            self.dismiss(color_name)
        elif event.key == "escape":
            self.dismiss(None)


# --- APLICACIÓN PRINCIPAL ---
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
        Binding("c", "change_color", "Cambiar Color"),
        Binding("n", "new_note", "Nueva Nota"),
        Binding("/", "focus_search", "Buscar"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main_container"):
            with Vertical(id="left_panel"):
                yield Static("🔍 Buscar notas... [ / ]", id="search_box")
                yield DirectoryTree("./notes", id="notes_tree")
            with Vertical(id="right_panel"):
                yield Markdown("# Selecciona una nota para leer\n\nPresiona `c` para asignar color.", id="viewer")
        yield Footer()

    def action_change_color(self) -> None:
        """Abre la paleta modal de colores."""
        def check_color(selected_color: str | None):
            if selected_color:
                self.notify(f"Color asignado: {selected_color}")
                # Aquí iría la lógica para actualizar el YAML Frontmatter del archivo actual

        self.push_screen(ColorPickerModal(), check_color)

    def action_focus_search(self) -> None:
        self.notify("Búsqueda activada (Fuzzy Search)")

if __name__ == "__main__":
    # Crear carpeta de pruebas si no existe
    os.makedirs("./notes", exist_ok=True)
    app = LazyNotesApp()
    app.run()