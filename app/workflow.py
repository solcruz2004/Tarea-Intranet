"""Funciones compartidas para ejecutar la automatización."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

from .config import get_settings
from .note_writer import prepare_paths, write_note
from .summarizer import SummarizationError, Summary, call_lm_studio
from .transcriber import TranscriptionResult, transcribe

logger = logging.getLogger(__name__)


@dataclass
class WorkflowResult:
    """Resultado final de la automatización."""

    note_path: Path
    transcript_path: Path
    summary: Summary
    transcription: TranscriptionResult


def run_workflow(
    audio_path: Path,
    title: str,
    class_date: date,
    notes_root: Optional[Path] = None,
    skip_summary: bool = False,
) -> WorkflowResult:
    """Ejecuta la transcripción y generación de notas."""

    audio_path = audio_path.expanduser().resolve()
    if not audio_path.exists():
        raise FileNotFoundError(f"El archivo de audio {audio_path} no existe")

    settings = get_settings()
    output_root = (notes_root or settings.notes_root).expanduser()
    output_root.mkdir(parents=True, exist_ok=True)

    final_title = title.strip() or audio_path.stem
    slug = _slugify(final_title)

    logger.info("Guardando notas en %s", output_root)

    transcription = transcribe(
        audio_path=audio_path,
        model_size=settings.whisper_model_size,
        compute_type=settings.whisper_compute_type,
        language=settings.whisper_language,
    )

    summary: Optional[Summary] = None
    if skip_summary:
        logger.warning("Se omitirá la generación de resumen por petición del usuario")
    else:
        logger.info(
            "Generando resumen con LM Studio usando el modelo %s", settings.lm_studio_model
        )
        try:
            summary = call_lm_studio(
                base_url=settings.lm_studio_base_url,
                model=settings.lm_studio_model,
                transcript=transcription.text,
                class_date=class_date.isoformat(),
                class_title=final_title,
            )
        except SummarizationError as exc:
            logger.error("No se pudo generar el resumen: %s", exc)
            logger.warning("La nota se creará únicamente con la transcripción.")

    if summary is None:
        summary = Summary(
            avance_clase=["Revisar transcripción adjunta."],
            tareas=[],
            pendientes=[],
            preguntas_examen=[],
        )

    paths = prepare_paths(output_root, class_date, slug)
    write_note(
        paths=paths,
        summary=summary,
        segments=transcription.segments,
        class_date=class_date,
        title=final_title,
        audio_name=audio_path.name,
        language=transcription.language,
        duration_minutes=transcription.duration / 60,
    )

    logger.info("Nota creada en %s", paths.note_path)
    logger.info("Transcripción detallada guardada en %s", paths.transcript_path)

    return WorkflowResult(
        note_path=paths.note_path,
        transcript_path=paths.transcript_path,
        summary=summary,
        transcription=transcription,
    )


def _slugify(value: str) -> str:
    normalized = value.strip().lower().replace(" ", "-")
    allowed = [c for c in normalized if c.isalnum() or c in {"-", "_"}]
    return "".join(allowed) or "clase"
