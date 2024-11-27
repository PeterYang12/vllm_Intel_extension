import sys
import os
import logging

logger = logging.getLogger(__name__)


def error_and_exit(error_message: str):
    """Logs an error message and exits with code 1"""
    logger.error(error_message)
    sys.exit(1)


def check_file_exist(file_path: str) -> bool:
    """Check if the file exists"""
    if not os.path.exists(file_path):
        error_and_exit(f"File not found at {file_path}")
    return True


def check_dir_exist(dir_path: str) -> bool:
    """Check if the directory exists"""
    if not os.path.exists(dir_path):
        error_and_exit(f"Directory not found at {dir_path}")
    return True