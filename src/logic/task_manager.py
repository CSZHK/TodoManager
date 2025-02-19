from db import database
import logging

# Create a logger
logger = logging.getLogger(__name__)

def add_task(title, description="", priority="medium", status="not_started", due_date=None, depends_on=None, parent_id=None):
    """Adds a new task to the database."""
    query = """
    INSERT INTO tasks (title, description, priority, status, due_date, depends_on, parent_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    database.execute(query, (title, description, priority, status, due_date, depends_on, parent_id))

def get_tasks():
    """Get all tasks from the database, ordered by hierarchy."""
    query = """
    SELECT * FROM tasks 
    ORDER BY 
        COALESCE(parent_id, id),
        CASE WHEN parent_id IS NULL THEN 0 ELSE 1 END,
        id
    """
    return database.fetch_all(query)

def update_task_status(task_id, status):
    """Updates the status of a task."""
    query = "UPDATE tasks SET status = ? WHERE id = ?"
    database.execute(query, (status, task_id))

def delete_task(task_id):
    """Deletes a task and its subtasks."""
    query = "DELETE FROM tasks WHERE id = ? OR parent_id = ?"
    database.execute(query, (task_id, task_id))

def delete_tasks(task_ids):
    """Delete multiple tasks by their IDs."""
    try:
        # First, delete any child tasks
        placeholders = ','.join(['?' for _ in task_ids])
        query = f"""
            DELETE FROM tasks 
            WHERE parent_id IN ({placeholders})
        """
        database.execute(query, task_ids)
        
        # Then delete the selected tasks
        query = f"""
            DELETE FROM tasks 
            WHERE id IN ({placeholders})
        """
        database.execute(query, task_ids)
        return True
    except Exception as e:
        print(f"Error deleting tasks: {e}")
        return False

def add_reminder(task_id, reminder_time):
    """Adds a reminder for a task."""
    database.add_reminder(task_id, reminder_time)

def get_reminders():
    """Retrieves all reminders from the database."""
    return database.get_reminders()

def calculate_progress():
    """Calculates the overall progress of all tasks."""
    tasks = get_tasks()
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task[4] == "completed")  # Assuming status is at index 4
    if total_tasks == 0:
        return 0
    return (completed_tasks / total_tasks) * 100

import re
from datetime import datetime

def parse_batch_tasks(text):
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
    database.execute(query, (
        parent_task["title"],
        parent_task["description"],
        parent_task["priority"],
        parent_task["status"],
        parent_task["due_date"],
        parent_task["depends_on"],
        parent_task["parent_id"]
    ))
    
    # Get the parent task ID
    parent_id = database.fetch_all("SELECT last_insert_rowid()")[0][0]
    
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
            database.execute(query, (
                subtask["title"],
                subtask["description"],
                subtask["priority"],
                subtask["status"],
                subtask["due_date"],
                subtask["depends_on"],
                subtask["parent_id"]
            ))
    
    return True

def clear_tasks():
    """Clear all tasks from the database."""
    try:
        database.execute("DELETE FROM tasks")
        return True
    except Exception as e:
        logger.error(f"Error clearing tasks: {e}")
        return False

if __name__ == '__main__':
    # Example Usage
    database.create_table()  # Make sure tables are created

    # Add a task
    task_id = add_task(
        title="Grocery Shopping",
        description="Buy groceries for the week",
        priority="high",
        status="not_started",
        due_date="2025-02-22",
        depends_on=None
    )
    print(f"Task added with ID: {task_id}")

    # Get all tasks
    tasks = get_tasks()
    print(f"Tasks: {tasks}")

    # Update task status
    update_task_status(task_id, "in_progress")
    print("Task status updated")

    # Calculate progress
    progress = calculate_progress()
    print(f"Progress: {progress}%")

    # Add a reminder
    add_reminder(task_id, "2025-02-21 18:00")
    print("Reminder added")

    # Get all reminders
    reminders = get_reminders()
    print(f"Reminders: {reminders}")
