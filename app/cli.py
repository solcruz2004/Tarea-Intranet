"""Punto de entrada de la línea de comandos."""

from __future__ import annotations

import argparse
import logging
from datetime import date, datetime
from pathlib import Path

from .config import get_settings
from .logger import get_logger, setup_logging
from .services import ServiceManager
from .workflow import run_workflow
from .logger import get_logger, setup_logging
from .workflow import run_workflow
from .config import get_settings
from .logger import get_logger, setup_logging
from .note_writer import prepare_paths, write_note
from .summarizer import SummarizationError, Summary, call_lm_studio
from .transcriber import TranscriptionResult, transcribe


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

    settings = get_settings()
    service_manager = ServiceManager(settings)

    def publish(status):
        level = logging.INFO if status.ready else logging.WARNING
        logger.log(level, "%s: %s", status.title, status.detail)

    service_manager.bootstrap_services(callback=publish)

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
    settings = get_settings()
    notes_root = parsed.notes_root or settings.notes_root
    notes_root.mkdir(parents=True, exist_ok=True)

    class_date = parse_date(parsed.date)
    slug = _slugify(parsed.title) if parsed.title else "clase"
    audio_path = parsed.audio.resolve()

    logger.info("Usando carpeta de notas: %s", notes_root)

    transcription: TranscriptionResult = transcribe(
        audio_path=audio_path,
        model_size=settings.whisper_model_size,
        compute_type=settings.whisper_compute_type,
        language=settings.whisper_language,
    )

    summary = None
    if parsed.skip_summary:
        logger.warning("Se omitió la generación de resumen por petición del usuario")
    else:
        try:
            summary = call_lm_studio(
                base_url=settings.lm_studio_base_url,
                model=settings.lm_studio_model,
                transcript=transcription.text,
                class_date=class_date.isoformat(),
                class_title=parsed.title,
            )
        except SummarizationError as exc:
            logger.error("No se pudo generar el resumen: %s", exc)
            logger.warning("La nota se creará solo con la transcripción.")

    if summary is None:
        summary = Summary(avance_clase=["Revisar transcripción adjunta."], tareas=[], pendientes=[], preguntas_examen=[])

    paths = prepare_paths(notes_root, class_date, slug)
    write_note(
        paths=paths,
        summary=summary,
        segments=transcription.segments,
        class_date=class_date,
        title=parsed.title,
        audio_name=audio_path.name,
        language=transcription.language,
        duration_minutes=transcription.duration / 60,
    )

    logger.info("Nota creada en %s", paths.note_path)
    logger.info("Transcripción detallada guardada en %s", paths.transcript_path)


def _slugify(value: str) -> str:
    normalized = value.strip().lower().replace(" ", "-")
    allowed = [c for c in normalized if c.isalnum() or c in {"-", "_"}]
    return "".join(allowed) or "clase"
