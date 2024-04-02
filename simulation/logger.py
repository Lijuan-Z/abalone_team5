import logging
import os
from datetime import datetime

log_directory = f"logs/simulation_logs/{datetime.now().strftime('%Y-%m-%d_%H-%M')}"

def create_logger(file_name):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    full_log_path = os.path.join(log_directory, file_name)

    # Create a custom logger
    logger = logging.getLogger(full_log_path )
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler(full_log_path)
    file_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)

    return logger
