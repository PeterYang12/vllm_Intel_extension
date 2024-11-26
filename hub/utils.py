import sys
import logging

logger = logging.getLogger(__name__)


def error_and_exit(error_message: str):
    """Logs an error message and exits with code 1"""
    logger.error(error_message)
    sys.exit(1)
