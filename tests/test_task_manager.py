import unittest
from src.db import database

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        # 创建测试数据库连接
        self.conn = database.create_connection()
        print(f"数据库地址: {database.DATABASE_PATH}")
        # 创建游标
        self.cursor = self.conn.cursor()
        # 创建测试表
        self.cursor.execute("""
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
        self.conn.commit()

    def tearDown(self):
        # 删除测试表
        self.cursor.execute("DROP TABLE IF EXISTS tasks")
        self.conn.commit()
        # 关闭数据库连接
        self.conn.close()

    def test_insert_and_get_tasks(self):
        # 插入父任务
        parent_id = database.insert_task("Parent Task", "Description", "High", "Not Started", "2025-02-22", None)
        self.assertIsNotNone(parent_id)

        # 插入子任务
        child1_id = database.insert_task("Child Task 1", "Description", "Medium", "In Progress", "2025-02-23", None, parent_id)
        self.assertIsNotNone(child1_id)
        child2_id = database.insert_task("Child Task 2", "Description", "Low", "Completed", "2025-02-24", None, parent_id)
        self.assertIsNotNone(child2_id)

        # 获取任务列表
        tasks = database.get_tasks()
        self.assertEqual(len(tasks), 1)

        # 验证父任务信息
        parent_task = tasks[0]
        self.assertEqual(parent_task["title"], "Parent Task")
        self.assertEqual(len(parent_task["children"]), 2)

        # 验证子任务信息
        child_task1 = parent_task["children"][0]
        self.assertEqual(child_task1["title"], "Child Task 1")
        child_task2 = parent_task["children"][1]
        self.assertEqual(child_task2["title"], "Child Task 2")

if __name__ == '__main__':
    unittest.main()
