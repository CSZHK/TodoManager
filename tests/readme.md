# 
python -c "from src.db import database; conn = database.create_connection(); print(f'数据库地址: {database.DATABASE_PATH}')"
数据库地址: /Users/atomstorm/Library/Application Support/AtomStorm/03_prototypes/TodoManager/tests/todo_manager.db

# 查表
sqlite3 C:\Users\Administrator\AppData\Roaming\TodoManager\tasks.db "SELECT id, title, status FROM tasks;"           
# 删库
sqlite3 C:\Users\Administrator\AppData\Roaming\TodoManager\tasks.db "DELETE FROM tasks;"