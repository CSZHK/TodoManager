# TodoManager

## 项目简介
TodoManager 是一个基于 PyQt6 的任务管理应用程序，支持任务的层级管理（父任务和子任务）以及任务状态的可视化展示。

## 核心功能
- 任务管理：创建、编辑、删除任务
- 支持父任务和子任务的层级关系
- 任务状态跟踪（未开始、进行中、已完成）
- 任务优先级设置
- 支持设置任务截止日期
- 现代化的用户界面，支持浅色/深色主题切换

## 最新更新 (2025-02-20)
### 任务显示优化
- 增强了任务状态的视觉区分：
  - 未开始：红色系
  - 进行中：橙色系
  - 已完成：绿色系

### 父子任务区分
- 父任务使用完整状态颜色，字体加粗，白色背景
- 子任务使用半透明状态颜色，斜体字体，浅灰色背景，缩进显示

### 系统改进
- 添加了详细的日志系统，包含任务处理的详细信息和错误追踪
- 优化了错误处理机制，单个任务处理失败不影响其他任务的显示

## 技术栈
- 前端：PyQt6
- 数据存储：SQLite3
- 开发语言：Python

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

## 使用说明
1. 克隆项目
2. 安装依赖
3. 运行应用程序

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
