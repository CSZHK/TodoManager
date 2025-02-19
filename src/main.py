import sys
from ui.main_window_qt import TaskManagerApp
from PyQt6.QtWidgets import QApplication
from db import database

if __name__ == "__main__":
    database.create_table()
    app = QApplication(sys.argv)
    window = TaskManagerApp()
    window.show()
    app.exec()
