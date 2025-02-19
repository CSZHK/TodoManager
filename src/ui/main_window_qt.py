from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QTableWidget,
    QTableWidgetItem, QMessageBox, QGroupBox, QHeaderView,
    QToolBar, QApplication, QMenu, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QFont, QColor
from logic import task_manager
from db import database

# Define theme stylesheets
LIGHT_THEME = """
    QMainWindow {
        background-color: #f5f5f5;
    }
    QGroupBox {
        border: 1px solid #ddd;
        border-radius: 6px;
        background-color: white;
        margin-top: 12px;
    }
    QGroupBox::title {
        color: #333;
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }
    QTableWidget {
        border: none;
        background-color: white;
        gridline-color: #f0f0f0;
        selection-background-color: #e3f2fd;
        selection-color: #000;
    }
    QTableWidget::item {
        padding: 5px;
        border-bottom: 1px solid #f0f0f0;
    }
    QTableWidget::item:alternate {
        background-color: #fafafa;
    }
    QHeaderView::section {
        background-color: white;
        padding: 5px;
        border: none;
        border-bottom: 2px solid #e0e0e0;
        font-weight: bold;
    }
    QPushButton {
        background-color: #f5f5f5;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 5px 15px;
        color: #333;
    }
    QPushButton:hover {
        background-color: #e0e0e0;
        border-color: #ccc;
    }
    QPushButton:pressed {
        background-color: #d0d0d0;
    }
    QLineEdit, QTextEdit {
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 5px;
        background-color: white;
    }
    QLineEdit:focus, QTextEdit:focus {
        border-color: #2196F3;
    }
    QLabel {
        color: #666;
    }
"""

DARK_THEME = """
    QMainWindow {
        background-color: #333;
    }
    QGroupBox {
        border: 1px solid #555;
        border-radius: 6px;
        background-color: #444;
        margin-top: 12px;
    }
    QGroupBox::title {
        color: #fff;
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }
    QTableWidget {
        border: none;
        background-color: #444;
        gridline-color: #555;
        selection-background-color: #666;
        selection-color: #fff;
    }
    QTableWidget::item {
        padding: 5px;
        border-bottom: 1px solid #555;
    }
    QTableWidget::item:alternate {
        background-color: #333;
    }
    QHeaderView::section {
        background-color: #444;
        padding: 5px;
        border: none;
        border-bottom: 2px solid #555;
        font-weight: bold;
    }
    QPushButton {
        background-color: #444;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 5px 15px;
        color: #fff;
    }
    QPushButton:hover {
        background-color: #555;
        border-color: #666;
    }
    QPushButton:pressed {
        background-color: #666;
    }
    QLineEdit, QTextEdit {
        border: 1px solid #555;
        border-radius: 4px;
        padding: 5px;
        background-color: #333;
    }
    QLineEdit:focus, QTextEdit:focus {
        border-color: #2196F3;
    }
    QLabel {
        color: #fff;
    }
"""

def get_theme_stylesheet(theme):
    return theme

def get_version_info():
    return "Task Manager v1.0"

class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        
        # Initialize theme
        self.current_theme = "light"
        self.themes = {"light": LIGHT_THEME, "dark": DARK_THEME}
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Initialize UI components
        self.setup_toolbar()
        self.setup_task_view(main_layout)
        self.create_edit_widgets()
        self.setup_footer(main_layout)
        
        # Add sections to main layout
        main_layout.addWidget(self.task_view_group, stretch=1)
        main_layout.addWidget(self.edit_section)
        main_layout.addWidget(self.batch_section)
        main_layout.addLayout(self.footer_layout)
        
        # Initially hide edit sections
        self.edit_section.hide()
        self.batch_section.hide()
        
        # Set window properties
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        # Apply theme
        self.apply_theme()
        
        # Load initial tasks
        self.load_tasks()

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme."""
        theme = self.themes[self.current_theme]
        self.setStyleSheet(get_theme_stylesheet(theme))
        
        # Update task colors based on theme
        self.load_tasks()

    def setup_toolbar(self):
        """Set up the toolbar with actions."""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Pin/Unpin action
        self.pin_action = QAction("📌", self)
        self.pin_action.setCheckable(True)
        self.pin_action.setChecked(True)
        self.pin_action.triggered.connect(self.toggle_pin)
        toolbar.addAction(self.pin_action)
        
        # Add edit mode toggle
        self.edit_action = QAction("✏️", self)
        self.edit_action.setCheckable(True)
        self.edit_action.setChecked(False)
        self.edit_action.triggered.connect(self.toggle_edit_mode)
        toolbar.addAction(self.edit_action)
        
        # Add theme toggle
        self.theme_action = QAction("🌓", self)
        self.theme_action.setCheckable(True)
        self.theme_action.setChecked(False)
        self.theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(self.theme_action)
        
        # Add version info
        version_label = QLabel(get_version_info())
        version_label.setStyleSheet("QLabel { padding: 5px; }")
        toolbar.addWidget(version_label)

    def setup_task_view(self, main_layout):
        """Set up the task viewing section."""
        self.task_view_group = QGroupBox("Tasks")
        task_view_layout = QVBoxLayout(self.task_view_group)
        task_view_layout.setSpacing(10)
        task_view_layout.setContentsMargins(15, 15, 15, 15)
        
        # Task table
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(["Title", "Description", "Status", "Due Date"])
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.task_table.setAlternatingRowColors(True)
        self.task_table.setShowGrid(False)
        self.task_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.task_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)  # Enable multi-select
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)  # Enable custom context menu
        self.task_table.customContextMenuRequested.connect(self.show_task_context_menu)
        task_view_layout.addWidget(self.task_table)
        
        # Status buttons
        status_layout = QHBoxLayout()
        status_layout.setSpacing(10)
        
        self.not_started_button = QPushButton("Not Started")
        self.in_progress_button = QPushButton("In Progress")
        self.completed_button = QPushButton("Completed")
        
        for btn in [self.not_started_button, self.in_progress_button, self.completed_button]:
            btn.setMinimumWidth(120)
            btn.setMinimumHeight(32)
        
        self.not_started_button.clicked.connect(lambda: self.update_status("not_started"))
        self.in_progress_button.clicked.connect(lambda: self.update_status("in_progress"))
        self.completed_button.clicked.connect(lambda: self.update_status("completed"))
        
        status_layout.addWidget(self.not_started_button)
        status_layout.addWidget(self.in_progress_button)
        status_layout.addWidget(self.completed_button)
        status_layout.addStretch()
        task_view_layout.addLayout(status_layout)

    def create_edit_widgets(self):
        """Create and set up the editing widgets."""
        # Task editing section
        self.edit_section = QGroupBox("Add/Edit Task")
        edit_layout = QVBoxLayout(self.edit_section)
        
        # Task input fields
        input_layout = QFormLayout()
        self.task_title_input = QLineEdit()
        self.task_description_input = QTextEdit()
        self.task_description_input.setMaximumHeight(100)  # Limit height
        input_layout.addRow("Title:", self.task_title_input)
        input_layout.addRow("Description:", self.task_description_input)
        
        # Add task button
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        
        edit_layout.addLayout(input_layout)
        edit_layout.addWidget(self.add_button)
        
        # Batch import section
        self.batch_section = QGroupBox("Batch Import")
        batch_layout = QVBoxLayout(self.batch_section)
        
        self.batch_import_text = QTextEdit()
        self.batch_import_text.setPlaceholderText("Enter tasks (first line is parent task, following lines are subtasks)")
        self.batch_import_text.setMaximumHeight(150)  # Limit height
        self.batch_import_button = QPushButton("Import Tasks")
        self.batch_import_button.clicked.connect(self.batch_import_tasks)
        
        batch_layout.addWidget(self.batch_import_text)
        batch_layout.addWidget(self.batch_import_button)

    def setup_footer(self, main_layout):
        """Set up the footer section with enhanced progress visualization."""
        self.footer_layout = QHBoxLayout()
        self.footer_layout.setSpacing(10)
        
        # Create progress section
        progress_widget = QWidget()
        progress_layout = QVBoxLayout(progress_widget)
        progress_layout.setSpacing(5)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMinimumWidth(200)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)
        
        # Status counts layout
        counts_layout = QHBoxLayout()
        counts_layout.setSpacing(15)
        
        # Total tasks
        self.total_label = QLabel()
        self.total_label.setStyleSheet("color: #666;")
        counts_layout.addWidget(self.total_label)
        
        # Completed tasks
        self.completed_label = QLabel()
        self.completed_label.setStyleSheet("color: #2e7d32; font-weight: bold;")
        counts_layout.addWidget(self.completed_label)
        
        # In progress tasks
        self.in_progress_label = QLabel()
        self.in_progress_label.setStyleSheet("color: #ef6c00; font-weight: bold;")
        counts_layout.addWidget(self.in_progress_label)
        
        # Not started tasks
        self.not_started_label = QLabel()
        self.not_started_label.setStyleSheet("color: #c62828; font-weight: bold;")
        counts_layout.addWidget(self.not_started_label)
        
        progress_layout.addLayout(counts_layout)
        
        # Add to footer
        self.footer_layout.addWidget(progress_widget)
        self.footer_layout.addStretch()
        
        # Clear button
        self.clear_button = QPushButton("Clear All Tasks")
        self.clear_button.setMinimumHeight(32)
        self.clear_button.clicked.connect(self.clear_tasks)
        self.footer_layout.addWidget(self.clear_button)

    def update_progress_display(self):
        """Update the progress display with current task statistics."""
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task[4] == "completed")
        in_progress_tasks = sum(1 for task in self.tasks if task[4] == "in_progress")
        not_started_tasks = sum(1 for task in self.tasks if task[4] == "not_started")
        
        # Update progress bar
        if total_tasks > 0:
            progress = (completed_tasks / total_tasks) * 100
            self.progress_bar.setValue(int(progress))
            
            # Change color based on progress
            if progress >= 80:
                chunk_color = "#4CAF50"  # Green
            elif progress >= 50:
                chunk_color = "#FFA726"  # Orange
            else:
                chunk_color = "#EF5350"  # Red
            
            self.progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    text-align: center;
                    height: 20px;
                }}
                QProgressBar::chunk {{
                    background-color: {chunk_color};
                    border-radius: 3px;
                }}
            """)
        else:
            self.progress_bar.setValue(0)
        
        # Update labels with task counts
        self.total_label.setText(f"Total: {total_tasks}")
        self.completed_label.setText(f"✓ Completed: {completed_tasks}")
        self.in_progress_label.setText(f"↻ In Progress: {in_progress_tasks}")
        self.not_started_label.setText(f"○ Not Started: {not_started_tasks}")

    def load_tasks(self):
        """Load tasks and display them in the table."""
        # Get tasks from database
        self.tasks = task_manager.get_tasks()
        
        # Clear the table first
        self.task_table.clearContents()
        self.task_table.setRowCount(0)
        
        # Set new row count
        self.task_table.setRowCount(len(self.tasks))
        
        for i, task in enumerate(self.tasks):
            # Unpack task data
            task_id, title, description, priority, status, due_date, depends_on, parent_id = task
            
            # Create title item with indentation for subtasks
            title_item = QTableWidgetItem()
            if parent_id is not None:  # This is a subtask
                title_item.setText("    ↳ " + title)  # Add indentation and arrow
                title_item.setForeground(Qt.GlobalColor.darkGray)
            else:  # This is a parent task
                title_item.setText(title)
                font = title_item.font()
                font.setBold(True)
                title_item.setFont(font)
            
            # Set task data
            self.task_table.setItem(i, 0, title_item)
            self.task_table.setItem(i, 1, QTableWidgetItem(description or ""))
            
            # Status with modern styling
            status_item = QTableWidgetItem()
            if status == "not_started":
                status_item.setText("○ Not Started")
                status_item.setBackground(QColor("#ffebee"))
                status_item.setForeground(QColor("#c62828"))
            elif status == "in_progress":
                status_item.setText("↻ In Progress")
                status_item.setBackground(QColor("#fff3e0"))
                status_item.setForeground(QColor("#ef6c00"))
            elif status == "completed":
                status_item.setText("✓ Completed")
                status_item.setBackground(QColor("#e8f5e9"))
                status_item.setForeground(QColor("#2e7d32"))
            self.task_table.setItem(i, 2, status_item)
            
            # Due date
            due_date_item = QTableWidgetItem(due_date or "")
            if due_date:
                due_date_item.setForeground(Qt.GlobalColor.darkBlue)
            self.task_table.setItem(i, 3, due_date_item)
        
        # Resize columns to content
        self.task_table.resizeColumnsToContents()
        self.task_table.horizontalHeader().setStretchLastSection(True)
        
        # Update progress display
        self.update_progress_display()

    def add_task(self):
        """Add a new task."""
        title = self.task_title_input.text().strip()
        description = self.task_description_input.toPlainText().strip()
        
        if not title:
            QMessageBox.warning(self, "Error", "Title is required.")
            return
        
        task_manager.add_task(
            title=title,
            description=description,
            priority="medium",
            status="not_started",
            due_date=None,
            depends_on=None,
            parent_id=None
        )
        
        # Clear inputs
        self.task_title_input.clear()
        self.task_description_input.clear()
        
        # Refresh the task list
        self.load_tasks()
        
        # Scroll to the bottom of the table
        self.task_table.scrollToBottom()
        
        # Select the newly added task
        last_row = self.task_table.rowCount() - 1
        self.task_table.selectRow(last_row)

    def update_status(self, status):
        selected_row = self.task_table.currentRow()
        if selected_row >= 0:
            task_id = self.tasks[selected_row][0]
            task_manager.update_task_status(task_id, status)
            self.load_tasks()
        else:
            QMessageBox.warning(self, "Error", "No task selected.")

    def clear_tasks(self):
        """Clear all tasks without confirmation."""
        try:
            database.execute("DELETE FROM tasks")
            self.load_tasks()  # Refresh task list
            
            # Show temporary success message
            self.total_label.setText("✓ All tasks cleared")
            self.total_label.setStyleSheet("color: #2e7d32; font-weight: bold;")
            
            # Reset the total label after 2 seconds
            QTimer.singleShot(2000, lambda: (
                self.total_label.setText("Total: 0"),
                self.total_label.setStyleSheet("color: #666;")
            ))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to clear tasks: {e}")

    def batch_import_tasks(self):
        """Imports tasks in bulk from the batch import text box."""
        text = self.batch_import_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Error", "No tasks to import.")
            return

        if task_manager.parse_batch_tasks(text):
            self.load_tasks()
            self.batch_import_text.clear()
        else:
            QMessageBox.warning(self, "Error", "Failed to import tasks.")

    def toggle_pin(self):
        flags = self.windowFlags()
        if self.pin_action.isChecked():
            flags |= Qt.WindowType.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()  # Need to show again after changing flags

    def toggle_edit_mode(self):
        """Toggle visibility of edit sections."""
        show = self.edit_action.isChecked()
        self.edit_section.setVisible(show)
        self.batch_section.setVisible(show)
        
        # Adjust window size smoothly
        if show:
            self.edit_section.setMaximumHeight(16777215)  # Remove height constraint
            self.batch_section.setMaximumHeight(16777215)
        else:
            self.edit_section.setMaximumHeight(0)
            self.batch_section.setMaximumHeight(0)

    def show_task_context_menu(self, position):
        """Show context menu for tasks."""
        menu = QMenu()
        
        # Get selected rows
        selected_rows = self.task_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        # Add delete action
        delete_text = "Delete Task" if len(selected_rows) == 1 else f"Delete {len(selected_rows)} Tasks"
        delete_action = QAction(delete_text, self)
        delete_action.triggered.connect(self.delete_selected_tasks)
        menu.addAction(delete_action)
        
        # Show menu at cursor position
        menu.exec(self.task_table.viewport().mapToGlobal(position))

    def delete_selected_tasks(self):
        """Delete all selected tasks without confirmation."""
        selected_rows = self.task_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        # Get task IDs from selected rows
        task_ids = []
        for row in selected_rows:
            task_id = self.tasks[row.row()][0]  # Get task ID from tasks list
            task_ids.append(task_id)
        
        # Delete tasks directly
        if task_manager.delete_tasks(task_ids):
            self.load_tasks()  # Refresh task list
            # Update total label temporarily to show deletion message
            original_text = self.total_label.text()
            self.total_label.setText(f"✓ Deleted {len(task_ids)} tasks")
            self.total_label.setStyleSheet("color: #2e7d32; font-weight: bold;")  # Green success color
            
            # Reset the total label after 2 seconds
            QTimer.singleShot(2000, lambda: (
                self.total_label.setText(original_text),
                self.total_label.setStyleSheet("color: #666;")
            ))
        else:
            QMessageBox.warning(self, "Error", "Failed to delete tasks")

if __name__ == "__main__":
    app = QApplication([])
    window = TaskManagerApp()
    window.show()
    app.exec()