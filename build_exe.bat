@echo off
pyinstaller --onefile --windowed --name TodoManager --icon=assets/icon.ico --add-data "src;src" --hidden-import sqlite3 src/main.py
pause
