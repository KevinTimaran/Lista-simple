import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Backend.logica_tareas import TaskLinkedList


class TaskAppTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Task List - Linked List")
        self.root.geometry("1080x680")
        self.root.resizable(False, False)

        self.task_list = TaskLinkedList()
        self.selected_task_id = None
        self.detail_panel_width = 360
        self.is_detail_panel_visible = False
        self.is_detail_panel_animating = False

        self._create_interface()
        self._refresh_screen()

    def _create_interface(self):
        title = tk.Label(
            self.root,
            text="Workshop: Task List with Linked List",
            font=("Arial", 13, "bold"),
            pady=10,
        )
        title.pack()

        add_frame = tk.Frame(self.root)
        add_frame.pack(pady=8, fill=tk.X, padx=16)

        tk.Label(add_frame, text="New task:", font=("Arial", 10)).grid(row=0, column=0, padx=5)

        self.task_input = tk.Entry(add_frame, width=52, font=("Arial", 10))
        self.task_input.grid(row=0, column=1, padx=5)

        add_button = tk.Button(
            add_frame,
            text="Add",
            command=self._add_task_from_ui,
            width=12,
            bg="#2e7d32",
            fg="white",
        )
        add_button.grid(row=0, column=2, padx=5)

        self.total_label = tk.Label(self.root, text="Total tasks: 0", font=("Arial", 10, "bold"))
        self.total_label.pack(pady=6)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        left_panel = tk.Frame(self.main_frame, bd=1, relief=tk.GROOVE)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(left_panel, text="Tasks", font=("Arial", 11, "bold")).pack(pady=8)

        self.tasks_canvas = tk.Canvas(left_panel, highlightthickness=0)
        self.tasks_scrollbar = tk.Scrollbar(left_panel, orient=tk.VERTICAL, command=self.tasks_canvas.yview)
        self.tasks_container = tk.Frame(self.tasks_canvas)

        self.tasks_container.bind(
            "<Configure>",
            lambda event: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all")),
        )
        self.tasks_canvas.create_window((0, 0), window=self.tasks_container, anchor="nw")
        self.tasks_canvas.configure(yscrollcommand=self.tasks_scrollbar.set)

        self.tasks_container.grid_columnconfigure(0, weight=1)
        self.tasks_container.grid_columnconfigure(1, weight=0)
        self.tasks_container.grid_columnconfigure(2, weight=1)

        self.pending_column = tk.Frame(self.tasks_container, bd=1, relief=tk.GROOVE, padx=6, pady=6)
        self.pending_column.grid(row=0, column=0, sticky="nsew", padx=(6, 3), pady=6)
        tk.Label(self.pending_column, text="Pending", font=("Arial", 10, "bold"), fg="#1d4ed8").pack(pady=(0, 6))
        self.pending_list_frame = tk.Frame(self.pending_column)
        self.pending_list_frame.pack(fill=tk.BOTH, expand=True)

        self.fixed_split_line = tk.Frame(self.tasks_container, width=2, bg="#9ca3af")
        self.fixed_split_line.grid(row=0, column=1, sticky="ns", pady=8)

        self.completed_column = tk.Frame(self.tasks_container, bd=1, relief=tk.GROOVE, padx=6, pady=6)
        self.completed_column.grid(row=0, column=2, sticky="nsew", padx=(3, 6), pady=6)
        tk.Label(self.completed_column, text="Completed", font=("Arial", 10, "bold"), fg="#047857").pack(pady=(0, 6))
        self.completed_list_frame = tk.Frame(self.completed_column)
        self.completed_list_frame.pack(fill=tk.BOTH, expand=True)

        self.tasks_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0), pady=(0, 8))
        self.tasks_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 8), pady=(0, 8))

        self.detail_panel = tk.Frame(self.main_frame, width=self.detail_panel_width, bd=1, relief=tk.GROOVE)
        self.detail_panel.pack_propagate(False)

        tk.Label(self.detail_panel, text="Task detail", font=("Arial", 11, "bold")).pack(pady=(10, 4))
        self.current_task_label = tk.Label(
            self.detail_panel,
            text="Select a task with the Details button",
            wraplength=320,
            justify=tk.LEFT,
            fg="#1f2937",
        )
        self.current_task_label.pack(padx=12, pady=(4, 10), anchor="w")

        tk.Label(self.detail_panel, text="Extra note:", font=("Arial", 10)).pack(padx=12, anchor="w")

        self.note_text = tk.Text(self.detail_panel, width=38, height=20, font=("Arial", 10))
        self.note_text.pack(padx=12, pady=(6, 10), fill=tk.BOTH, expand=True)

        self.save_note_button = tk.Button(
            self.detail_panel,
            text="Save note",
            command=self._save_note_from_ui,
            state=tk.DISABLED,
            bg="#6d28d9",
            fg="white",
            width=16,
        )
        self.save_note_button.pack(pady=(0, 10))

        self.main_frame.update_idletasks()
        self.detail_panel.place(x=self._get_hidden_panel_x(), y=0, width=self.detail_panel_width, relheight=1.0)

        note = tk.Label(
            self.root,
            text="Note: by workshop requirement, task deletion is not included.",
            fg="#555555",
            font=("Arial", 9),
        )
        note.pack(pady=(0, 8))

    def _add_task_from_ui(self):
        description = self.task_input.get().strip()

        if description == "":
            messagebox.showwarning("Invalid data", "You must write a description.")
            return

        self.task_list.add_task(description)
        self.task_input.delete(0, tk.END)
        self.selected_task_id = None
        self._refresh_screen()

    def _get_visible_panel_x(self):
        return max(0, self.main_frame.winfo_width() - self.detail_panel_width)

    def _get_hidden_panel_x(self):
        return self.main_frame.winfo_width() + 20

    def _animate_panel(self, target_x):
        if self.is_detail_panel_animating:
            return

        self.is_detail_panel_animating = True

        def step():
            current_x = self.detail_panel.winfo_x()
            difference = target_x - current_x

            if abs(difference) <= 14:
                self.detail_panel.place_configure(x=target_x)
                self.is_detail_panel_animating = False
                return

            step_size = 14 if difference > 0 else -14
            self.detail_panel.place_configure(x=current_x + step_size)
            self.root.after(8, step)

        step()

    def _show_detail_panel(self):
        self.is_detail_panel_visible = True
        self._animate_panel(self._get_visible_panel_x())

    def _hide_detail_panel(self):
        self.is_detail_panel_visible = False
        self._animate_panel(self._get_hidden_panel_x())

    def _clear_detail_panel(self):
        self.current_task_label.config(text="Select a task with the Details button")
        self.note_text.delete("1.0", tk.END)
        self.save_note_button.config(state=tk.DISABLED)

    def _mark_task_from_ui(self, task_id):
        found = self.task_list.mark_completed(task_id)

        if not found:
            messagebox.showinfo("Not found", "There is no task with that ID.")

        self._refresh_screen()

    def _open_detail_panel(self, task_id):
        task = self.task_list.find_task(task_id)

        if task is None:
            messagebox.showinfo("Not found", "There is no task with that ID.")
            return

        self.selected_task_id = task_id
        status = "Completed" if task.completed else "Pending"
        self.current_task_label.config(text=f"ID {task.id}: {task.description}\nStatus: {status}")

        self.note_text.delete("1.0", tk.END)
        self.note_text.insert(tk.END, task.note)
        self.save_note_button.config(state=tk.NORMAL)
        self._show_detail_panel()

    def _save_note_from_ui(self):
        if self.selected_task_id is None:
            messagebox.showwarning("Selection required", "First choose a task with Details.")
            return

        note = self.note_text.get("1.0", tk.END).strip()
        saved = self.task_list.save_note(self.selected_task_id, note)

        if not saved:
            messagebox.showinfo("Not found", "There is no task with that ID.")
            return

        self._refresh_screen()
        self._hide_detail_panel()
        self.selected_task_id = None
        self._clear_detail_panel()
        messagebox.showinfo("Saved", "Note saved correctly.")

    def _clear_task_visual_list(self):
        for widget in self.pending_list_frame.winfo_children():
            widget.destroy()

        for widget in self.completed_list_frame.winfo_children():
            widget.destroy()

    def _draw_tasks(self):
        self._clear_task_visual_list()

        current = self.task_list.head
        pending_count = 0
        completed_count = 0

        if current is None:
            empty_label = tk.Label(self.pending_list_frame, text="No tasks created.", fg="#4b5563")
            empty_label.pack(pady=12)

            empty_completed_label = tk.Label(self.completed_list_frame, text="No completed tasks.", fg="#4b5563")
            empty_completed_label.pack(pady=12)
            return

        while current is not None:
            status = "Completed" if current.completed else "Pending"
            status_color = "#047857" if current.completed else "#1d4ed8"

            target_frame = self.completed_list_frame if current.completed else self.pending_list_frame
            row = tk.Frame(target_frame, bd=1, relief=tk.SOLID, padx=8, pady=8)
            row.pack(fill=tk.X, padx=8, pady=5)

            if current.completed:
                completed_count += 1
            else:
                pending_count += 1

            title_label = tk.Label(
                row,
                text=f"ID {current.id} | {current.description}",
                font=("Arial", 10, "bold"),
                anchor="w",
            )
            title_label.grid(row=0, column=0, sticky="w")

            status_label = tk.Label(row, text=status, fg=status_color, font=("Arial", 9, "bold"))
            status_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

            details_button = tk.Button(
                row,
                text="Details",
                command=lambda task_id=current.id: self._open_detail_panel(task_id),
                width=10,
                bg="#2563eb",
                fg="white",
            )
            details_button.grid(row=0, column=1, padx=5)

            complete_button = tk.Button(
                row,
                text="Complete",
                command=lambda task_id=current.id: self._mark_task_from_ui(task_id),
                width=10,
                bg="#0f766e",
                fg="white",
            )
            if current.completed:
                complete_button.config(state=tk.DISABLED)
            complete_button.grid(row=1, column=1, padx=5, pady=(4, 0))

            current = current.next

        if pending_count == 0:
            empty_pending_label = tk.Label(self.pending_list_frame, text="No pending tasks.", fg="#4b5563")
            empty_pending_label.pack(pady=12)

        if completed_count == 0:
            empty_completed_label = tk.Label(self.completed_list_frame, text="No completed tasks.", fg="#4b5563")
            empty_completed_label.pack(pady=12)

    def _refresh_screen(self):
        self.total_label.config(text=f"Total tasks: {self.task_list.size}")
        self._draw_tasks()

        if self.selected_task_id is not None and self.is_detail_panel_visible:
            task = self.task_list.find_task(self.selected_task_id)
            if task is not None:
                status = "Completed" if task.completed else "Pending"
                self.current_task_label.config(text=f"ID {task.id}: {task.description}\nStatus: {status}")
                self.note_text.delete("1.0", tk.END)
                self.note_text.insert(tk.END, task.note)


def main():
    root = tk.Tk()
    app = TaskAppTkinter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
