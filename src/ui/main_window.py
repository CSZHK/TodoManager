import tkinter as tk
from tkinter import ttk
from logic import task_manager
import logging

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        self.tasks = []
        self.task_id_counter = 1

        self.init_ui()
        self.load_tasks()

    def init_ui(self):
        # Task List Frame
        self.task_list_frame = ttk.Frame(self.root)
        self.task_list_frame.pack(pady=10)

        # Task List
        self.task_list = tk.Listbox(self.task_list_frame, width=50, height=10)
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.task_list_frame, orient=tk.VERTICAL, command=self.task_list.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_list['yscrollcommand'] = self.scrollbar.set

        # Add Task Frame
        self.add_task_frame = ttk.Frame(self.root)
        self.add_task_frame.pack(pady=10)

        # Task Title
        self.title_label = ttk.Label(self.add_task_frame, text="Title:")
        self.title_label.grid(row=0, column=0, padx=5)
        self.title_entry = ttk.Entry(self.add_task_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)

        # Task Description
        self.description_label = ttk.Label(self.add_task_frame, text="Description:")
        self.description_label.grid(row=1, column=0, padx=5)
        self.description_entry = ttk.Entry(self.add_task_frame, width=30)
        self.description_entry.grid(row=1, column=1, padx=5)

        # Add Task Button
        self.add_button = ttk.Button(self.add_task_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=2, column=1, padx=5, pady=5)

        # Status Buttons Frame
        self.status_buttons_frame = ttk.Frame(self.root)
        self.status_buttons_frame.pack(pady=10)

        # Status Buttons
        self.not_started_button = ttk.Button(self.status_buttons_frame, text="Not Started", command=lambda: self.update_status("not_started"))
        self.not_started_button.grid(row=0, column=0, padx=5)

        self.in_progress_button = ttk.Button(self.status_buttons_frame, text="In Progress", command=lambda: self.update_status("in_progress"))
        self.in_progress_button.grid(row=0, column=1, padx=5)

        self.completed_button = ttk.Button(self.status_buttons_frame, text="Completed", command=lambda: self.update_status("completed"))
        self.completed_button.grid(row=0, column=2, padx=5)

    def load_tasks(self):
        self.tasks = task_manager.get_tasks()
        self.update_task_list()

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        task_id = task_manager.add_task(title=title, description=description, priority="medium", status="not_started", due_date=None, depends_on=None)
        self.load_tasks()
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def update_status(self, status):
        """Updates the status of the selected task."""
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            task_id = self.tasks[selected_task_index[0]][0]
            logging.info(f"Updating status for task ID: {task_id} to status: {status}")
            task_manager.update_task_status(task_id, status)
            self.load_tasks()
        else:
            logging.warning("No task selected for status update")

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.tasks:
            task_id, title, _, _, status, _, _ = task
            task_text = f"[{task_id}] {title} - {status}"
            self.task_list.insert(tk.END, task_text)
            # Set color based on status
            if status == "not_started":
                self.task_list.itemconfig(tk.END, bg="lightcoral")
            elif status == "in_progress":
                self.task_list.itemconfig(tk.END, bg="lightyellow")
            elif status == "completed":
                self.task_list.itemconfig(tk.END, bg="lightgreen")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
