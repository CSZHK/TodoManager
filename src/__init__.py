import logging
import logging.handlers

# Configure logging
logger = logging.getLogger('TodoManager')
logger.setLevel(logging.DEBUG)

# Create file handler
file_handler = logging.handlers.RotatingFileHandler(
    'todo_manager.log',
    maxBytes=1024*1024,  # 1MB
    backupCount=3
)
file_handler.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add formatter to handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
