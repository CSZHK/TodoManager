import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent / "tasks.db"


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as e:
        print(e)

    return conn

def fetch_all(query, params=()):
    """Executes a SQL query and returns all results."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def create_table():
    """Creates the tasks table if it doesn't exist."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        # Drop existing table to ensure correct schema
        cursor.execute("DROP TABLE IF EXISTS tasks")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT,
                status TEXT,
                due_date TEXT,
                depends_on INTEGER,
                parent_id INTEGER,
                FOREIGN KEY(parent_id) REFERENCES tasks(id)
            )
        """)
        conn.commit()

def execute(query, params=()):
    """Executes a SQL query."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

def insert_task(title, description, priority, status, due_date, depends_on):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, description, priority, status, due_date, depends_on)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, description, priority, status, due_date, depends_on))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def get_tasks():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task_status(task_id, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks SET status = ? WHERE id = ?
    """, (status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def add_reminder(task_id, reminder_time):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reminders (task_id, reminder_time)
        VALUES (?, ?)
    """, (task_id, reminder_time))
    conn.commit()
    conn.close()

def get_reminders():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reminders")
    reminders = cursor.fetchall()
    conn.close()
    return reminders

if __name__ == '__main__':
    create_table()
    # Example usage
    # task_id = insert_task("Test Task", "Description", "high", "not_started", "2025-02-20", None)
    # print(f"Inserted task with id: {task_id}")
    # tasks = get_tasks()
    # print(f"Tasks: {tasks}")
    # update_task_status(task_id, "in_progress")
    # print("Updated task status")
    # delete_task(task_id)
    # print("Deleted task")
