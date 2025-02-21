import sqlite3
import os
import logging
from pathlib import Path


# Get user's data directory
if os.name == 'nt':  # Windows
    DATA_DIR = Path(os.getenv('APPDATA')) / "TodoManager"
else:  # Linux/Mac
    DATA_DIR = Path.home() / ".TodoManager"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATA_DIR / "tasks.db"

logger = logging.getLogger(__name__)

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        print(f"Connected to SQLite database at {DATABASE_PATH}")
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
        # 添加索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_parent_id ON tasks(parent_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
        conn.commit()

def execute(query, params=()):
    """Executes a SQL query."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

def insert_task(title, description, priority, status, due_date, depends_on, parent_id=None):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, description, priority, status, due_date, depends_on, parent_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, description, priority, status, due_date, depends_on, parent_id))
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
    task_dict = {}
    for task in tasks:
        task_id, title, description, priority, status, due_date, depends_on, parent_id = task
        if parent_id is None:
            task_dict[task_id] = {
                'id': task_id,
                'title': title,
                'description': description,
                'priority': priority,
                'status': status,
                'due_date': due_date,
                'depends_on': depends_on,
                'children': []
            }
        else:
            # 只在parent_id存在于task_dict中时添加子任务
            if parent_id in task_dict:
                task_dict[parent_id]['children'].append({
                    'id': task_id,
                    'title': title,
                    'description': description,
                    'priority': priority,
                    'status': status,
                    'due_date': due_date,
                    'depends_on': depends_on,
                    'children': []
                })
            else:
                # 处理parent_id不在task_dict中的情况
                task_dict[parent_id] = {
                    'id': parent_id,
                    'title': 'Unknown Parent',
                    'children': [{
                        'id': task_id,
                        'title': title,
                        'description': description,
                        'priority': priority,
                        'status': status,
                        'due_date': due_date,
                        'depends_on': depends_on,
                        'children': []
                    }]
                }
    return list(task_dict.values())

def update_task_status(task_id, status):
    logger.debug(f"正在更新任务{task_id}状态为{status}")
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    logger.debug(f"受影响行数: {cursor.rowcount}")
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
