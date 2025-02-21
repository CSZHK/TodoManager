# TodoManager

一个基于Python和PyQt6的现代化任务管理系统。

## 功能特点

- 支持任务层级管理（父任务和子任务）
- 任务状态实时更新
- 批量任务导入
- 多选任务操作
- 任务优先级管理
- 直观的用户界面

## 系统要求

- Python 3.8+
- PyQt6
- SQLite3

## 安装说明

1. 克隆仓库：
```bash
git clone [repository-url]
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用说明

1. 启动应用：
```bash
python src/main.py
```

2. 基本操作：
   - 添加任务：点击"添加任务"按钮
   - 更新状态：选择任务后点击对应状态按钮
   - 删除任务：选择任务后点击"删除"按钮
   - 导入任务：支持批量导入，使用缩进表示任务层级

3. 任务层级管理：
   - 父任务：最高层级任务
   - 子任务：通过缩进或设置父任务ID创建
   - 支持多级任务结构

4. 状态管理：
   - 待办（Todo）
   - 进行中（In Progress）
   - 已完成（Done）
   - 已取消（Cancelled）

## 最新更新

- 修复子任务状态更新问题
- 优化任务层级显示
- 改进多选操作功能
- 增强批量导入功能

## 开发说明

详细的开发文档和API参考请查看 `docs` 目录。

## 许可证

本项目采用 MIT 许可证。

## 项目结构
```
TodoManager/
├── src/
│   ├── ui/
│   │   └── main_window_qt.py    # 主窗口和UI逻辑
│   ├── logic/
│   │   └── task_manager.py      # 任务管理逻辑
│   └── db/
│       └── database.py          # 数据库操作
├── README.md                    # 项目说明
└── note.md                      # 开发笔记
```

## 待办事项
- 实现任务提醒功能
- 添加任务标签/分类功能
- 实现任务导入/导出功能
- 添加任务统计和报告功能
- 优化数据库查询性能

## 已知问题
- 无

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TodoManager.git
cd TodoManager
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python src/db/database.py
```

5. Run the application:
```bash
python src/main.py
```

## Packaging

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Create the executable:
```bash
pyinstaller --onefile --windowed --name TodoManager --icon=assets/icon.ico --add-data "src;src" --hidden-import sqlite3 src/main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
