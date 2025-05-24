# logger.py
import logging
import os

def get_logger(name=__name__):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers in interactive environments
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(f"{log_dir}/sync.log", encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add handler
        logger.addHandler(file_handler)

    return logger
