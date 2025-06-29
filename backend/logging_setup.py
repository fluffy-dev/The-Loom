import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging(
    log_file: str = "app.log",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    sqlalchemy_level: int = logging.WARNING, # Уменьшаем "шум" от SQLAlchemy
    uvicorn_level: int = logging.INFO,
    file_bytes_size: int = 10 * 1024 * 1024, # 10 MB
    backup_count: int = 10,
) -> None:
    """
    Configures logging for the entire application.

    Sets up handlers for both console output and file rotation,
    and configures levels for different parts of the application.

    Args:
        log_file (str): The name of the file to log to.
        console_level (int): The logging level for console output.
        file_level (int): The logging level for file output.
        sqlalchemy_level (int): The logging level for SQLAlchemy engine logs.
        uvicorn_level (int): The logging level for Uvicorn server logs.
        file_bytes_size (int): Maximum size of a log file before rotation.
        backup_count (int): The number of backup log files to keep.
    """
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=file_bytes_size,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

    logging.getLogger("sqlalchemy.engine").setLevel(sqlalchemy_level)
    logging.getLogger("uvicorn.error").setLevel(uvicorn_level)
    logging.getLogger("uvicorn.access").setLevel(uvicorn_level)

    logging.info("Logging initialized successfully.")