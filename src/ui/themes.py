"""Theme management for TodoManager."""

LIGHT_THEME = {
    "window_bg": "#f5f5f5",
    "widget_bg": "white",
    "text": "#333333",
    "text_secondary": "#666666",
    "border": "#dddddd",
    "hover_bg": "#e0e0e0",
    "pressed_bg": "#d0d0d0",
    "selection_bg": "#e3f2fd",
    "selection_text": "#000000",
    "accent": "#2196F3",
    "status_not_started": {"bg": "#ffebee", "fg": "#c62828"},
    "status_in_progress": {"bg": "#fff3e0", "fg": "#ef6c00"},
    "status_completed": {"bg": "#e8f5e9", "fg": "#2e7d32"},
}

DARK_THEME = {
    "window_bg": "#1e1e1e",
    "widget_bg": "#2d2d2d",
    "text": "#ffffff",
    "text_secondary": "#cccccc",
    "border": "#404040",
    "hover_bg": "#404040",
    "pressed_bg": "#505050",
    "selection_bg": "#0d47a1",
    "selection_text": "#ffffff",
    "accent": "#64b5f6",
    "status_not_started": {"bg": "#4a1515", "fg": "#ff5252"},
    "status_in_progress": {"bg": "#4a3000", "fg": "#ffb74d"},
    "status_completed": {"bg": "#1b5e20", "fg": "#69f0ae"},
}

def get_theme_stylesheet(theme):
    """Generate stylesheet for the given theme."""
    return f"""
        QMainWindow {{
            background-color: {theme["window_bg"]};
        }}
        QGroupBox {{
            border: 1px solid {theme["border"]};
            border-radius: 6px;
            background-color: {theme["widget_bg"]};
            margin-top: 12px;
            color: {theme["text"]};
        }}
        QGroupBox::title {{
            color: {theme["text"]};
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
        QTableWidget {{
            border: none;
            background-color: {theme["widget_bg"]};
            gridline-color: {theme["border"]};
            selection-background-color: {theme["selection_bg"]};
            selection-color: {theme["selection_text"]};
            color: {theme["text"]};
        }}
        QTableWidget::item {{
            padding: 5px;
            border-bottom: 1px solid {theme["border"]};
        }}
        QTableWidget::item:alternate {{
            background-color: {theme["window_bg"]};
        }}
        QHeaderView::section {{
            background-color: {theme["widget_bg"]};
            padding: 5px;
            border: none;
            border-bottom: 2px solid {theme["border"]};
            color: {theme["text"]};
            font-weight: bold;
        }}
        QPushButton {{
            background-color: {theme["widget_bg"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            padding: 5px 15px;
            color: {theme["text"]};
        }}
        QPushButton:hover {{
            background-color: {theme["hover_bg"]};
        }}
        QPushButton:pressed {{
            background-color: {theme["pressed_bg"]};
        }}
        QLineEdit, QTextEdit {{
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            padding: 5px;
            background-color: {theme["widget_bg"]};
            color: {theme["text"]};
        }}
        QLineEdit:focus, QTextEdit:focus {{
            border-color: {theme["accent"]};
        }}
        QLabel {{
            color: {theme["text_secondary"]};
        }}
        QToolBar {{
            spacing: 5px;
            padding: 5px;
            background: transparent;
            border: none;
        }}
        QToolButton {{
            font-size: 16px;
            padding: 5px;
            border: none;
            border-radius: 4px;
            background: transparent;
            color: {theme["text"]};
        }}
        QToolButton:hover {{
            background: {theme["hover_bg"]};
        }}
        QToolButton:checked {{
            background: {theme["pressed_bg"]};
        }}
    """
