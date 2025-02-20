import sys
import os

# Add src directory to Python path
if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    sys.path.append(os.path.join(sys._MEIPASS, 'src'))
else:
    # Running in development mode
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ui.main_window_qt import TaskManagerApp
from PyQt6.QtWidgets import QApplication
from db import database
from logic.task_manager import TaskManager

if __name__ == "__main__":
    database.create_table()
    task_manager = TaskManager()
    app = QApplication(sys.argv)
    window = TaskManagerApp(task_manager)
    window.show()
    app.exec()
