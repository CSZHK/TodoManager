from PyQt6.QtWidgets import (
    QMainWindow, QTableWidgetItem, QMessageBox, QMenu,
    QToolBar, QApplication, QProgressBar, QStyledItemDelegate,
    QListWidgetItem, QListWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QTableWidget, QGroupBox, QHeaderView,
    QFormLayout
)
from PyQt6.QtCore import Qt, QTimer, QRect, QModelIndex
from PyQt6.QtGui import QAction, QFont, QPainter, QPen, QColor, QIcon
from logic import task_manager
from db import database
import logging

# 配置日志记录
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   handlers=[
                       logging.FileHandler('todo_manager.log'),
                       logging.StreamHandler()
                   ])

logger = logging.getLogger(__name__)

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

class TaskItemDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index):
        super().paint(painter, option, index)
        
        # 绘制进行中任务的左边框高亮
        if index.data(Qt.ItemDataRole.UserRole) == "in_progress":
            painter.save()
            pen = QPen(QColor("#FF8C00"), 3)  # 3像素宽的橙色边框
            painter.setPen(pen)
            rect = option.rect
            # 只绘制左边框
            painter.drawLine(rect.topLeft(), rect.bottomLeft())
            painter.restore()

class TaskManagerApp(QMainWindow):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.setWindowTitle("Task Manager")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        
        # Initialize theme
        self.current_theme = "light"
        self.themes = {"light": LIGHT_THEME, "dark": DARK_THEME}
        
        # Initialize tasks list
        self.tasks = []
        self.flat_tasks = []
        
        # 定义状态样式
        self.status_styles = {
            'Not Started': {
                'color': '#FF4D4D',
                'icon': '⭕',
                'background': '#FFF0F0',
                'text_color': '#D32F2F',
                'parent_background': '#FFE0E0',
                'parent_text_color': '#B71C1C'
            },
            'In Progress': {
                'color': '#FF8C00',
                'icon': '⏳',
                'background': '#FFF4E6',
                'text_color': '#2196F3',
                'parent_background': '#FFE8CC',
                'parent_text_color': '#1976D2'
            },
            'Completed': {
                'color': '#4CAF50',
                'icon': '✅',
                'background': '#E8F5E9',
                'text_color': '#388E3C',
                'parent_background': '#C8E6C9',
                'parent_text_color': '#1B5E20'
            }
        }
        
        # 定义任务层级样式
        self.task_hierarchy_styles = {
            'parent': {
                'background': '#FFFFFF',  # 白色背景
                'font_weight': 'bold',    # 加粗
                'indent': ''              # 无缩进
            },
            'child': {
                'background': '#F8F9FA',  # 浅灰色背景
                'font_style': 'italic',   # 斜体
                'indent': '    ',       # 缩进
                'text_color': '#666666'   # 深灰色文字
            }
        }
        
        # 初始化UI组件
        self._init_ui()
        
    def _init_ui(self):
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
        
        # Apply theme and load tasks
        self.apply_theme()
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

        # 设置表格样式
        self.task_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #E0E0E0;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #E0E0E0;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: black;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                font-weight: bold;
            }
        """)
        
        # 设置表头
        header = self.task_table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        header.setStretchLastSection(True)
        
        # 设置行高
        self.task_table.verticalHeader().setDefaultSectionSize(40)

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
        """Updates the progress bar and label based on completed tasks."""
        if not self.tasks:
            total = 0
            completed = 0
        else:
            total = len(self.tasks)
            completed = sum(1 for task in self.tasks if task['status'] == 'completed')
        
        # Calculate percentage
        percentage = (completed / total * 100) if total > 0 else 0
        
        # Update progress bar
        self.progress_bar.setValue(int(percentage))
        
        # Update status label with modern styling
        self.total_label.setText(f"Total: {total} | Completed: {completed}")
        
        # Set color based on progress
        if percentage >= 80:
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    background: #E8F5E9;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background: #4CAF50;
                    border-radius: 5px;
                }
            """)
        elif percentage >= 50:
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    background: #FFF3E0;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background: #FF9800;
                    border-radius: 5px;
                }
            """)
        else:
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    background: #FFEBEE;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background: #F44336;
                    border-radius: 5px;
                }
            """)

    def load_tasks(self):
        """Load tasks and display them in the table."""
        # Get tasks from database
        self.tasks = self.task_manager.get_tasks()
        
        # 展开任务层级为平面列表
        self.flat_tasks = []
        def flatten_tasks(tasks, level=0):
            for task in tasks:
                task['_level'] = level  # 添加层级信息
                self.flat_tasks.append(task)
                if 'children' in task:
                    flatten_tasks(task['children'], level + 1)
        
        flatten_tasks(self.tasks)
        self.task_table.setRowCount(len(self.flat_tasks))
        
        for row, task in enumerate(self.flat_tasks):
            try:
                logger.debug(f"处理任务: ID={task['id']}, 标题={task['title']}, 父任务ID={task.get('parent_id')}")
                
                # 标准化状态并设置样式
                status = task['status'].replace('_', ' ').title()
                status_style = self.status_styles.get(status, {})
                logger.debug(f"任务状态: {status}, 样式: {status_style}")
                
                # 设置标题
                title_item = QTableWidgetItem()
                indent = "    " * task['_level']
                arrow = "→ " if task['_level'] > 0 else ""
                title_item.setText(f"{indent}{arrow}{task['title']}")
                
                # 设置父/子任务样式
                if task['_level'] > 0:
                    title_item.setForeground(QColor("#666666"))
                    title_item.setIcon(QIcon(':/icons/subtask.png'))
                else:
                    font = title_item.font()
                    font.setBold(True)
                    title_item.setFont(font)
                
                self.task_table.setItem(row, 0, title_item)
                
                # 设置描述
                desc_item = QTableWidgetItem(task.get('description', '') or '')
                desc_item.setForeground(QColor("#666666"))
                self.task_table.setItem(row, 1, desc_item)
                
                # 设置状态
                status_item = QTableWidgetItem(status)
                status_item.setForeground(QColor(status_style.get('color', 'black')))
                self.task_table.setItem(row, 2, status_item)
                
                # 根据状态设置行背景颜色
                for j in range(self.task_table.columnCount()):
                    item = self.task_table.item(row, j)
                    if item:
                        if task['status'] == 'not_started':
                            item.setBackground(QColor('#FFEBEE'))  # 浅红色
                            item.setForeground(QColor(status_style.get('text_color', '#D32F2F')))  # 红色字体
                        elif task['status'] == 'in_progress':
                            item.setBackground(QColor('#FFF3E0'))  # 浅橙色
                            item.setForeground(QColor('#2196F3'))  # 蓝色字体
                        elif task['status'] == 'completed':
                            item.setBackground(QColor('#E8F5E9'))  # 浅绿色
                            item.setForeground(QColor(status_style.get('text_color', '#2E7D32')))  # 绿色字体
        
                # Due date
                due_date = task.get('due_date', '')
                due_date_item = QTableWidgetItem(due_date if due_date else "")
                if due_date:
                    due_date_item.setForeground(QColor("#1976D2"))
                self.task_table.setItem(row, 3, due_date_item)

            except Exception as e:
                logger.error(f"处理任务时出错: {e}", exc_info=True)
                continue  # 跳过处理出错的任务，继续处理下一个
                
        logger.info("任务显示更新完成")
        
        # Update progress display
        self.update_progress_display()
        
        # Resize columns to content
        self.task_table.resizeColumnsToContents()
        self.task_table.horizontalHeader().setStretchLastSection(True)

    def add_task(self):
        """Add a new task."""
        title = self.task_title_input.text().strip()
        description = self.task_description_input.toPlainText().strip()
        
        if not title:
            QMessageBox.warning(self, "Error", "Title is required.")
            return
        
        self.task_manager.add_task(
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
        """Updates the status of the selected task."""
        selected_rows = self.task_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "错误", "请先选择要更新的任务！")
            return

        task_ids = []
        for row in selected_rows:
            row_idx = row.row()
            if 0 <= row_idx < len(self.flat_tasks):
                task_ids.append(self.flat_tasks[row_idx]['id'])
        
        logger.debug(f"待更新任务ID列表: {task_ids}")
        
        for task_id in task_ids:
            self.task_manager.update_task_status(task_id, status)
        
        self.load_tasks()

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
            QMessageBox.warning(self, "错误", "请输入要批量添加的任务！")
            return
        
        lines = text.split('\n')
        current_parent_id = None
        tasks_added = 0
        
        for line in lines:
            original_line = line
            line = line.rstrip()  # 保留左侧空格，去除右侧空格
            if not line:
                continue
            
            # 计算缩进级别（每个缩进是4个空格）
            indent_level = len(line) - len(line.lstrip())
            is_subtask = indent_level >= 4
            title = line.strip()
            
            if is_subtask:
                if current_parent_id is None:
                    QMessageBox.warning(self, "错误", "子任务前必须有父任务！")
                    return
                # 添加子任务
                self.task_manager.add_task(
                    title=title,
                    description='',
                    priority='medium',
                    status='not_started',
                    due_date=None,
                    depends_on=None,
                    parent_id=current_parent_id
                )
            else:
                # 添加父任务
                current_parent_id = self.task_manager.add_task(
                    title=title,
                    description='',
                    priority='medium',
                    status='not_started',
                    due_date=None,
                    depends_on=None,
                    parent_id=None
                )
            tasks_added += 1
        
        # 刷新任务列表
        self.load_tasks()
        self.batch_import_text.clear()
        QMessageBox.information(self, "成功", f"成功导入 {tasks_added} 个任务！")

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
        # 获取当前编辑按钮的状态
        show = self.edit_action.isChecked()
        
        # 设置编辑区域和批量导入区域的可见性
        self.edit_section.setVisible(show)
        self.batch_section.setVisible(show)
        
        # 调整窗口大小
        if show:
            # 显示编辑区域时，移除高度限制
            self.edit_section.setMaximumHeight(16777215)
            self.batch_section.setMaximumHeight(16777215)
        else:
            # 隐藏编辑区域时，设置高度为0
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
            QMessageBox.warning(self, "错误", "请先选择要删除的任务！")
            return
        
        # 获取平面化后的任务列表
        task_ids = [self.flat_tasks[row.row()]['id'] for row in selected_rows if row.row() < len(self.flat_tasks)]
        
        if task_ids:
            # Delete tasks
            for task_id in task_ids:
                self.task_manager.delete_task(task_id)
            
            # Refresh the task list
            self.load_tasks()
            
            # Show success message
            QMessageBox.information(self, "成功", f"已删除 {len(task_ids)} 个任务！")

    def update_task_display(self):
        """更新任务显示，包含详细的日志记录"""
        try:
            logger.info("开始更新任务显示")
            # 获取所有任务
            self.tasks = self.task_manager.get_tasks()
            
            # 展开任务层级为平面列表
            self.flat_tasks = []
            def flatten_tasks(tasks, level=0):
                for task in tasks:
                    task['_level'] = level  # 添加层级信息
                    self.flat_tasks.append(task)
                    if 'children' in task:
                        flatten_tasks(task['children'], level + 1)
            
            flatten_tasks(self.tasks)
            self.task_table.setRowCount(len(self.flat_tasks))
            logger.debug(f"获取到 {len(self.flat_tasks)} 个任务")
            
            for row, task in enumerate(self.flat_tasks):
                try:
                    logger.debug(f"处理任务: ID={task['id']}, 标题={task['title']}, 父任务ID={task.get('parent_id')}")
                    
                    # 标准化状态并设置样式
                    status = task['status'].replace('_', ' ').title()
                    status_style = self.status_styles.get(status, {})
                    logger.debug(f"任务状态: {status}, 样式: {status_style}")
                    
                    # 设置标题
                    title_item = QTableWidgetItem()
                    indent = "    " * task['_level']
                    arrow = "→ " if task['_level'] > 0 else ""
                    title_item.setText(f"{indent}{arrow}{task['title']}")
                    
                    # 设置父/子任务样式
                    if task['_level'] > 0:
                        title_item.setForeground(QColor("#666666"))
                        title_item.setIcon(QIcon(':/icons/subtask.png'))
                    else:
                        font = title_item.font()
                        font.setBold(True)
                        title_item.setFont(font)
                    
                    self.task_table.setItem(row, 0, title_item)
                    
                    # 设置描述
                    desc_item = QTableWidgetItem(task.get('description', '') or '')
                    desc_item.setForeground(QColor("#666666"))
                    self.task_table.setItem(row, 1, desc_item)
                    
                    # 设置状态
                    status_item = QTableWidgetItem(status)
                    status_item.setForeground(QColor(status_style.get('color', 'black')))
                    self.task_table.setItem(row, 2, status_item)
                    
                    # 根据状态设置行背景颜色
                    for j in range(self.task_table.columnCount()):
                        item = self.task_table.item(row, j)
                        if item:
                            if task['status'] == 'not_started':
                                item.setBackground(QColor('#FFEBEE'))  # 浅红色
                                item.setForeground(QColor(status_style.get('text_color', '#D32F2F')))  # 红色字体
                            elif task['status'] == 'in_progress':
                                item.setBackground(QColor('#FFF3E0'))  # 浅橙色
                                item.setForeground(QColor('#2196F3'))  # 蓝色字体
                            elif task['status'] == 'completed':
                                item.setBackground(QColor('#E8F5E9'))  # 浅绿色
                                item.setForeground(QColor(status_style.get('text_color', '#2E7D32')))  # 绿色字体
        
                    # Due date
                    due_date = task.get('due_date', '')
                    due_date_item = QTableWidgetItem(due_date if due_date else "")
                    if due_date:
                        due_date_item.setForeground(QColor("#1976D2"))
                    self.task_table.setItem(row, 3, due_date_item)

                except Exception as e:
                    logger.error(f"处理任务时出错: {e}", exc_info=True)
                    continue  # 跳过处理出错的任务，继续处理下一个
                    
            logger.info("任务显示更新完成")
            
        except Exception as e:
            logger.error(f"更新任务显示时出错: {e}", exc_info=True)
            raise

    def update_task_display_with_hierarchy(self):
        """更新任务显示，包含详细的日志记录和任务层级"""
        try:
            logger.info("开始更新任务显示")
            tasks = self.task_manager.get_tasks()
            self.task_table.setRowCount(len(tasks))
            logger.debug(f"获取到 {len(tasks)} 个任务")
            
            for row, task in enumerate(tasks):
                try:
                    # 解包任务数据
                    task_id, title, description, priority, status, due_date, depends_on, parent_id = task
                    logger.debug(f"处理任务: ID={task_id}, 标题={title}, 父任务ID={parent_id}")
                    
                    # 标准化状态并设置样式
                    status = status.replace('_', ' ').title()
                    status_style = self.status_styles.get(status, {})
                    logger.debug(f"任务状态: {status}, 样式: {status_style}")
                    
                    # 设置标题
                    title_item = QTableWidgetItem(title)
                    self.task_table.setItem(row, 0, title_item)
                    
                    # 设置描述
                    desc_item = QTableWidgetItem(description or "")
                    desc_item.setForeground(QColor("#666666"))
                    self.task_table.setItem(row, 1, desc_item)
                    
                    # 设置状态
                    status_item = QTableWidgetItem(f"{status}")
                    status_item.setForeground(QColor(status_style.get('color', 'black')))
                    self.task_table.setItem(row, 2, status_item)
                    
                    # 设置到期日期
                    due_date_item = QTableWidgetItem(due_date or "")
                    self.task_table.setItem(row, 3, due_date_item)
                    
                    # 应用任务层级样式
                    style = self.task_hierarchy_styles['child' if parent_id else 'parent']
                    logger.debug(f"应用{'子' if parent_id else '父'}任务样式")
                    
                    # 设置标题样式
                    if parent_id:  # 子任务
                        title_item.setText("    " + title)
                        font = title_item.font()
                        font.setItalic(True)
                        title_item.setFont(font)
                        # 子任务使用状态颜色但透明度降低
                        color = QColor(status_style.get('text_color', '#666666'))
                        color.setAlpha(200)  # 设置透明度
                        title_item.setForeground(color)
                    else:  # 父任务
                        font = title_item.font()
                        font.setBold(True)
                        title_item.setFont(font)
                        # 父任务使用完整状态颜色
                        title_item.setForeground(QColor(status_style.get('text_color', '#000000')))
                    
                    # 设置整行样式
                    for col in range(self.task_table.columnCount()):
                        item = self.task_table.item(row, col)
                        if item:
                            # 设置背景色
                            item.setBackground(QColor(style['background']))
                            # 设置文字颜色（状态列除外）
                            if col != 2:  # 不是状态列
                                if parent_id:
                                    # 子任务使用状态颜色但透明度降低
                                    color = QColor(status_style.get('text_color', '#666666'))
                                    color.setAlpha(200)
                                    item.setForeground(color)
                                else:
                                    # 父任务使用完整状态颜色
                                    item.setForeground(QColor(status_style.get('text_color', '#000000')))
                    
                    # 如果是进行中的任务，设置字体加粗
                    if status == 'In Progress':
                        for col in range(self.task_table.columnCount()):
                            item = self.task_table.item(row, col)
                            if item:
                                font = item.font()
                                font.setBold(True)
                                item.setFont(font)
                                
                except Exception as e:
                    logger.error(f"处理任务时出错: {e}", exc_info=True)
                    continue  # 跳过处理出错的任务，继续处理下一个
                    
            logger.info("任务显示更新完成")
            
        except Exception as e:
            logger.error(f"更新任务显示时出错: {e}", exc_info=True)
            raise

    def _show_status_sync_notification(self, parent_task, new_status):
        """Shows a notification when child tasks are synced to a new status."""
        QMessageBox.information(self, 'Status Sync', f'Child tasks of "{parent_task["title"]}" have been synced to "{new_status}".')

if __name__ == "__main__":
    app = QApplication([])
    window = TaskManagerApp(task_manager)
    window.show()
    app.exec()