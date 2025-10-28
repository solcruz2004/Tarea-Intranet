"""Módulo encargado de convertir archivos de audio en texto."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)


@dataclass
class Segment:
    """Representa un segmento de texto transcrito."""

    start: float
    end: float
    text: str


@dataclass
class TranscriptionResult:
    """Resultado completo de la transcripción."""

    text: str
    segments: Iterable[Segment]
    language: str
    duration: float


def transcribe(
    audio_path: Path,
    model_size: str,
    compute_type: str = "auto",
    language: Optional[str] = None,
    device: str = "cpu",
) -> TranscriptionResult:
    """Transcribe un archivo de audio utilizando Faster Whisper."""

    logger.info("Cargando modelo de Whisper (%s)...", model_size)
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    logger.info("Iniciando transcripción de %s", audio_path)
    segments_iter, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=5,
        vad_filter=True,
    )

    segments = [Segment(start=s.start, end=s.end, text=s.text.strip()) for s in segments_iter]
    text = " ".join(segment.text for segment in segments).strip()

    logger.info(
        "Transcripción finalizada. Idioma detectado: %s. Duración: %.2f minutos.",
        info.language,
        info.duration / 60,
    )

    return TranscriptionResult(
        text=text,
        segments=segments,
        language=info.language,
        duration=info.duration,
    )


def segments_to_markdown(segments: Iterable[Segment]) -> str:
    """Convierte los segmentos en una tabla legible en Markdown."""

    lines = ["| Inicio | Fin | Texto |", "|-------|-----|-------|"]
    for segment in segments:
        clean_text = segment.text.replace("|", "\\|")
        lines.append(
            f"| {format_timestamp(segment.start)} | {format_timestamp(segment.end)} | {clean_text} |"
        )
    return "\n".join(lines)


def format_timestamp(seconds: float) -> str:
    """Formatea segundos a un timestamp HH:MM:SS."""

    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
