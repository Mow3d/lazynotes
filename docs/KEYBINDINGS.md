# ⌨️ LazyNotes — Keybindings Reference

This document defines the key mapping for navigating, managing and editing notes in **LazyNotes**. The configuration follows **Vim**-style modal usage and the speed of TUI tools like **LazyVim** and **LazyGit**.

---

## 1. Global Shortcuts (available in any panel)

| Key | Action | Description |
| :--- | :--- | :--- |
| `Tab` | Switch Panel | Moves focus between the **Explorer** and the **Viewer/Editor**. |
| `/` | Fuzzy Search | Focuses the top search bar (*Telescope*-style). |
| `?` | Help Menu | Shows this floating window with the available shortcuts. |
| `q` | Quit | Closes the application. |

---

## 2. Notes Explorer (`NOTES EXPLORER`)

| Key | Action | Description |
| :--- | :--- | :--- |
| `j` / `↓` | Move Down | Moves the selection to the note or folder below. |
| `k` / `↑` | Move Up | Moves the selection to the note or folder above. |
| `l` / `Enter` | Open / Expand | Expands a folder or loads the selected note in the viewer. |
| `h` | Collapse / Up | Collapses the current folder or moves up a level in the tree. |
| `n` | New Note | Opens the prompt to create a note in the active category. |
| `c` | Assign Color | Opens the color palette modal for the note. |
| `d` | Delete Note | Moves the selected note to `Trash/` (soft delete). |
| `1` - `3` | Quick Jump | Jumps directly to the corresponding numbered root category. |

---

## 3. Read Mode (`NOTE VIEWER`)

| Key | Action | Description |
| :--- | :--- | :--- |
| `j` / `k` | Scroll | Scrolls the rendered content up or down. |
| `e` / `Enter` | Enter Edit Mode | Switches the active view to the embedded text editor (`TextArea`). |
| `c` | Assign Color | Opens the color palette for the loaded note. |
| `d` | Delete Note | Moves the active note to the `Trash/` folder. |

---

## 4. Edit Mode (`NOTE EDITOR` / `TextArea`)

| Key | Action | Description |
| :--- | :--- | :--- |
| `Ctrl + S` | Save | Applies the changes, updates `modified` in the YAML and returns to the viewer. |
| `Esc` | Cancel | Cancels the current edit and returns to read mode without saving. |

---

## 5. Modal Windows and Search

| Key | Action | Description |
| :--- | :--- | :--- |
| `1` - `7` | Quick Selection | Directly picks the color number inside the `c` modal. |
| `Esc` | Close / Clear | Clears the search filter or closes the active modal window. |
| `Enter` | Confirm | Selects the filtered result or confirms the change. |
