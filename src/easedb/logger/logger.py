from loguru import logger as loguru_logger
import os
import sys
from pathlib import Path

# Globális logoló objektum
logger = loguru_logger

def create_log_directory(base_dir="logs"):
    """
    Creates the directory structure for logs.
    """
    base_path = Path(base_dir)
    json_dir = base_path / "json"
    readable_dir = base_path / "readable"

    # Create directories if they don't exist
    json_dir.mkdir(parents=True, exist_ok=True)
    readable_dir.mkdir(parents=True, exist_ok=True)

    return json_dir, readable_dir


def setup_logger(level: str = "WARNING", base_dir="logs", use_structure=False):
    """
    Sets up the default logger with both console and file handlers.
    If use_structure is True, logs will be saved in the structured directories.
    """
    # Remove existing handlers
    logger.remove()

    # Console logging with default Loguru format
    logger.add(sys.stdout, 
               level=level,
               colorize=True)

    if use_structure:
        # Create log directories
        json_dir, readable_dir = create_log_directory(base_dir)

        # File logging - readable logs
        logger.add(readable_dir / "easedb.log", 
                   rotation="5 MB",
                   retention="7 days",
                   compression="zip",
                   level=level)

        # File logging - JSON format
        logger.add(json_dir / "easedb.json", 
                   rotation="5 MB",
                   retention="7 days",
                   compression="zip",
                   serialize=True,  # JSON serialization
                   level=level)

# Publikus metódus konfiguráláshoz
def logger_config(level: str = "INFO", base_dir="logs", use_structure=False):
    setup_logger(level, base_dir, use_structure)
    logger.info(f"Logger initialized with level: {level}, use_structure: {use_structure}")
