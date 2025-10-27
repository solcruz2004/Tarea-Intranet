"""Punto de entrada de la línea de comandos."""

from __future__ import annotations

import argparse
import logging
from datetime import date, datetime
from pathlib import Path

from .logger import get_logger, setup_logging
from .workflow import run_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Automatización de apuntes desde audio")
    parser.add_argument(
        "audio",
        type=Path,
        help="Ruta al archivo de audio (cualquier formato soportado por ffmpeg)",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Fecha de la clase en formato YYYY-MM-DD. Por defecto se usa la fecha actual.",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Clase sin título",
        help="Título o asignatura de la clase.",
    )
    parser.add_argument(
        "--notes-root",
        type=Path,
        default=None,
        help="Carpeta donde se guardarán las notas (sobrescribe NOTES_ROOT).",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Nivel de detalle del logging.",
    )
    parser.add_argument(
        "--skip-summary",
        action="store_true",
        help="No llamar a LM Studio y generar una nota con la transcripción únicamente.",
    )
    return parser


def parse_date(raw_date: str | None) -> date:
    if raw_date is None:
        return date.today()
    return datetime.strptime(raw_date, "%Y-%m-%d").date()


def main(args: list[str] | None = None) -> None:
    parser = build_parser()
    parsed = parser.parse_args(args)

    setup_logging(getattr(logging, parsed.log_level))
    logger = get_logger(__name__)

    if not parsed.audio.exists():
        parser.error(f"El archivo {parsed.audio} no existe")

    class_date = parse_date(parsed.date)
    result = run_workflow(
        audio_path=parsed.audio,
        title=parsed.title,
        class_date=class_date,
        notes_root=parsed.notes_root,
        skip_summary=parsed.skip_summary,
    )

    logger.info(
        "\n¡Listo! Abre Obsidian en %s para revisar tus apuntes.", result.note_path.parent
    )
