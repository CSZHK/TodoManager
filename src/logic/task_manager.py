from db import database
import logging

# Create a logger
logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self):
        self.db = database

    def add_task(self, title, description="", priority="medium", status="not_started", due_date=None, depends_on=None, parent_id=None):
        """Adds a new task to the database."""
        return self.db.insert_task(title, description, priority, status, due_date, depends_on, parent_id)

    def get_tasks(self):
        """Retrieves all tasks with hierarchy information."""
        tasks = self.db.fetch_all("SELECT * FROM tasks ORDER BY parent_id, id")
        # 将元组转换为字典
        columns = ['id', 'title', 'description', 'priority', 'status', 'due_date', 'depends_on', 'parent_id']
        tasks = [dict(zip(columns, task)) for task in tasks]
        return self._build_task_hierarchy(tasks)

    def _build_task_hierarchy(self, tasks):
        """Builds a hierarchical structure of tasks."""
        task_map = {task['id']: task for task in tasks}
        root_tasks = []
        for task in tasks:
            if task['parent_id'] is None:
                root_tasks.append(task)
            else:
                parent = task_map.get(task['parent_id'])
                if parent:
                    if 'children' not in parent:
                        parent['children'] = []
                    parent['children'].append(task)
        return root_tasks

    def update_task_status(self, task_id, new_status):
        """Updates the status of a task and its children."""
        # 更新当前任务状态
        self.db.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        # 递归更新子任务状态
        self._update_child_task_status(task_id, new_status)

    def _update_child_task_status(self, parent_id, new_status):
        """Recursively updates the status of child tasks."""
        children = self.db.fetch_all("SELECT id FROM tasks WHERE parent_id = ?", (parent_id,))
        for child in children:
            self.db.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, child[0]))
            self._update_child_task_status(child[0], new_status)

    def delete_task(self, task_id):
        """Deletes a task and its subtasks."""
        query = "DELETE FROM tasks WHERE id = ? OR parent_id = ?"
        self.db.execute(query, (task_id, task_id))

    def delete_tasks(self, task_ids):
        """Delete multiple tasks by their IDs."""
        try:
            # First, delete any child tasks
            placeholders = ','.join(['?' for _ in task_ids])
            query = f"""
                DELETE FROM tasks 
                WHERE parent_id IN ({placeholders})
            """
            self.db.execute(query, task_ids)
            
            # Then delete the selected tasks
            query = f"""
                DELETE FROM tasks 
                WHERE id IN ({placeholders})
            """
            self.db.execute(query, task_ids)
            return True
        except Exception as e:
            print(f"Error deleting tasks: {e}")
            return False

    def add_reminder(self, task_id, reminder_time):
        """Adds a reminder for a task."""
        self.db.add_reminder(task_id, reminder_time)

    def get_reminders(self):
        """Retrieves all reminders from the database."""
        return self.db.get_reminders()

    def calculate_progress(self):
        """Calculates the overall progress of all tasks."""
        tasks = self.get_tasks()
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task['status'] == "completed")  
        if total_tasks == 0:
            return 0
        return (completed_tasks / total_tasks) * 100

    def parse_batch_tasks(self, text):
        """Parses a batch of tasks from the input text."""
        tasks = []
        lines = text.strip().split("\n")
        if not lines:
            return tasks

        # First line is the parent task
        parent_task = {
            "title": lines[0].strip(),
            "description": "",
            "priority": "medium",
            "status": "not_started",
            "due_date": None,
            "depends_on": None,
            "parent_id": None
        }
        
        # Add parent task
        query = """
        INSERT INTO tasks (title, description, priority, status, due_date, depends_on, parent_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.db.execute(query, (
            parent_task["title"],
            parent_task["description"],
            parent_task["priority"],
            parent_task["status"],
            parent_task["due_date"],
            parent_task["depends_on"],
            parent_task["parent_id"]
        ))
        
        # Get the parent task ID
        parent_id = self.db.fetch_all("SELECT last_insert_rowid()")[0][0]
        
        # Add subtasks
        for line in lines[1:]:
            if line.strip():
                subtask = {
                    "title": line.strip(),
                    "description": "",
                    "priority": "medium",
                    "status": "not_started",
                    "due_date": None,
                    "depends_on": None,
                    "parent_id": parent_id
                }
                self.db.execute(query, (
                    subtask["title"],
                    subtask["description"],
                    subtask["priority"],
                    subtask["status"],
                    subtask["due_date"],
                    subtask["depends_on"],
                    subtask["parent_id"]
                ))
        
        return True

    def clear_tasks(self):
        """Clear all tasks from the database."""
        try:
            self.db.execute("DELETE FROM tasks")
            return True
        except Exception as e:
            logger.error(f"Error clearing tasks: {e}")
            return False

if __name__ == '__main__':
    # Example Usage
    task_manager = TaskManager()
    task_manager.db.create_table()  # Make sure tables are created

    # Add a task
    task_manager.add_task(
        title="Grocery Shopping",
        description="Buy groceries for the week",
        priority="high",
        status="not_started",
        due_date="2025-02-22",
        depends_on=None
    )
    print("Task added")

    # Get all tasks
    tasks = task_manager.get_tasks()
    print(f"Tasks: {tasks}")

    # Update task status
    task_manager.update_task_status(1, "in_progress")
    print("Task status updated")

    # Calculate progress
    progress = task_manager.calculate_progress()
    print(f"Progress: {progress}%")

    # Add a reminder
    task_manager.add_reminder(1, "2025-02-21 18:00")
    print("Reminder added")

    # Get all reminders
    reminders = task_manager.get_reminders()
    print(f"Reminders: {reminders}")
