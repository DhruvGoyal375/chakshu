import logging
import logging.handlers
from pathlib import Path

from django.conf import settings

from .utils import get_env_variable


def setup_logger(name):
    """
    Set up a logger with both file and console handlers.

    Args:
        name (str): Name of the logger, typically __name__

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path(settings.BASE_DIR) / "logs"
    log_dir.mkdir(exist_ok=True, parents=True)

    # Get the logger
    logger = logging.getLogger(name)
    logger.setLevel(get_env_variable("LOG_LEVEL", "INFO").upper())

    # Prevent adding handlers multiple times in case setup is called more than once
    if logger.handlers:
        return logger

    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Create logs directory if it doesn't exist
    log_file = log_dir / "chakshu.log"

    # File handler - Rotating file based on size (10MB per file, keep 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(get_env_variable("LOG_LEVEL", "INFO").upper())
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(get_env_variable("LOG_LEVEL", "INFO").upper())
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
