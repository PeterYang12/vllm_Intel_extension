import sys
import logging

logger = logging.getLogger(__name__)

# Logs an error message and exits with code 1
def error_and_exit(error_message: str):
    logger.error(error_message)
    sys.exit(1)