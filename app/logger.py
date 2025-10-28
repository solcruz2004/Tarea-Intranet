"""Configuración básica de logging con Rich."""

from __future__ import annotations

import logging
from rich.console import Console
from rich.logging import RichHandler


def setup_logging(level: int = logging.INFO) -> None:
    """Configura el logging para la aplicación."""

    console = Console()
    handler = RichHandler(console=console, show_time=True, show_path=False)
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[handler],
    )


get_logger = logging.getLogger
