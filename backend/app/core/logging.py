"""Logging configuration."""

import logging
import sys
from typing import Any

from backend.app.config import settings


def setup_logging() -> None:
    """Configure application logging."""

    # Set log level based on environment
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Configure uvicorn loggers
    logging.getLogger("uvicorn").setLevel(log_level)
    logging.getLogger("uvicorn.access").setLevel(log_level)
    logging.getLogger("uvicorn.error").setLevel(log_level)

    # Configure sqlalchemy logger (only show warnings in production)
    sqlalchemy_level = logging.DEBUG if settings.DEBUG else logging.WARNING
    logging.getLogger("sqlalchemy.engine").setLevel(sqlalchemy_level)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
