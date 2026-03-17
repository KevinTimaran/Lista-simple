import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sys

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
if str(RUTA_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RUTA_PROYECTO))

from Backend.logica_tareas import ListaEnlazadaTareas


class AppTareasTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas - Lista Enlazada")
        self.root.geometry("580x420")
        self.root.resizable(False, False)

        self.lista_tareas = ListaEnlazadaTareas()

        self._crear_interfaz()
        self._refrescar_pantalla()

    def _crear_interfaz(self):
        titulo = tk.Label(
            self.root,
            text="Taller: Lista de Tareas con Lista Enlazada",
            font=("Arial", 13, "bold"),
            pady=10,
        )
        titulo.pack()

        frame_agregar = tk.Frame(self.root)
        frame_agregar.pack(pady=8)

        tk.Label(frame_agregar, text="Nueva tarea:", font=("Arial", 10)).grid(row=0, column=0, padx=5)

        self.entrada_tarea = tk.Entry(frame_agregar, width=38, font=("Arial", 10))
        self.entrada_tarea.grid(row=0, column=1, padx=5)

        btn_agregar = tk.Button(
            frame_agregar,
            text="Agregar",
            command=self._agregar_tarea_desde_ui,
            width=12,
            bg="#2e7d32",
            fg="white",
        )
        btn_agregar.grid(row=0, column=2, padx=5)

        frame_marcar = tk.Frame(self.root)
        frame_marcar.pack(pady=8)

        tk.Label(frame_marcar, text="ID a completar:", font=("Arial", 10)).grid(row=0, column=0, padx=5)

        self.entrada_id = tk.Entry(frame_marcar, width=10, font=("Arial", 10))
        self.entrada_id.grid(row=0, column=1, padx=5)

        btn_marcar = tk.Button(
            frame_marcar,
            text="Marcar completada",
            command=self._marcar_tarea_desde_ui,
            width=16,
            bg="#1565c0",
            fg="white",
        )
        btn_marcar.grid(row=0, column=2, padx=5)

        self.label_total = tk.Label(self.root, text="Total de tareas: 0", font=("Arial", 10, "bold"))
        self.label_total.pack(pady=8)

        self.area_tareas = tk.Text(self.root, width=68, height=14, font=("Consolas", 10))
        self.area_tareas.pack(padx=12, pady=8)
        self.area_tareas.config(state=tk.DISABLED)

        nota = tk.Label(
            self.root,
            text="Nota: por requerimiento del taller, no se incluye funcion para eliminar tareas.",
            fg="#555555",
            font=("Arial", 9),
        )
        nota.pack(pady=4)

    def _agregar_tarea_desde_ui(self):
        descripcion = self.entrada_tarea.get().strip()

        if descripcion == "":
            messagebox.showwarning("Dato invalido", "Debes escribir una descripcion.")
            return

        self.lista_tareas.agregar_tarea(descripcion)
        self.entrada_tarea.delete(0, tk.END)
        self._refrescar_pantalla()

    def _marcar_tarea_desde_ui(self):
        valor_id = self.entrada_id.get().strip()

        if valor_id == "" or not valor_id.isdigit():
            messagebox.showwarning("Dato invalido", "Debes escribir un ID numerico.")
            return

        identificador = int(valor_id)
        encontrada = self.lista_tareas.marcar_completada(identificador)

        if not encontrada:
            messagebox.showinfo("No encontrada", "No existe una tarea con ese ID.")

        self.entrada_id.delete(0, tk.END)
        self._refrescar_pantalla()

    def _refrescar_pantalla(self):
        self.label_total.config(text=f"Total de tareas: {self.lista_tareas.tamano}")

        texto = self.lista_tareas.construir_texto_tareas()
        self.area_tareas.config(state=tk.NORMAL)
        self.area_tareas.delete("1.0", tk.END)
        self.area_tareas.insert(tk.END, texto)
        self.area_tareas.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = AppTareasTkinter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
