"""Creación de notas en formato Markdown compatibles con Obsidian."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

from .summarizer import Summary
from .transcriber import Segment, segments_to_markdown


@dataclass
class NotePaths:
    """Rutas generadas para los archivos del día."""

    note_path: Path
    transcript_path: Path


NOTE_TEMPLATE = """---
date: {date_iso}
title: {title}
audio_source: {audio_name}
language: {language}
duration_minutes: {duration:.2f}
---

# {title} ({date_human})

## Resumen estructurado

### Avance de clase
{avance}

### Tareas asignadas
{tareas}

### Pendientes y recordatorios
{pendientes}

### Preguntas para el examen
{preguntas}

## Transcripción completa

El detalle por segmentos se encuentra en el archivo relacionado: [[{transcript_rel}]].
"""

TRANSCRIPT_TEMPLATE = """# Transcripción - {title} ({date_human})

Archivo de audio: {audio_name}
Idioma detectado: {language}
Duración: {duration:.2f} minutos

{table}
"""


def prepare_paths(notes_root: Path, class_date: date, slug: str) -> NotePaths:
    """Crea las carpetas necesarias y devuelve las rutas de nota y transcripción."""

    year_folder = notes_root / str(class_date.year)
    month_folder = year_folder / f"{class_date.month:02d}"
    transcripts_folder = month_folder / "transcripciones"
    month_folder.mkdir(parents=True, exist_ok=True)
    transcripts_folder.mkdir(parents=True, exist_ok=True)

    note_filename = f"{class_date.isoformat()}-{slug}.md"
    transcript_filename = f"{class_date.isoformat()}-{slug}-transcripcion.md"

    return NotePaths(
        note_path=month_folder / note_filename,
        transcript_path=transcripts_folder / transcript_filename,
    )


def write_note(
    paths: NotePaths,
    summary: Summary,
    segments: Iterable[Segment],
    class_date: date,
    title: str,
    audio_name: str,
    language: str,
    duration_minutes: float,
) -> None:
    """Escribe la nota y el archivo de transcripción detallado."""

    note_content = NOTE_TEMPLATE.format(
        date_iso=class_date.isoformat(),
        title=title,
        audio_name=audio_name,
        language=language,
        duration=duration_minutes,
        date_human=class_date.strftime("%d de %B de %Y"),
        avance=_list_to_markdown(summary.avance_clase),
        tareas=_list_to_markdown(summary.tareas),
        pendientes=_list_to_markdown(summary.pendientes),
        preguntas=_list_to_markdown(summary.preguntas_examen),
        transcript_rel=paths.transcript_path.name,
    )

    transcript_content = TRANSCRIPT_TEMPLATE.format(
        title=title,
        date_human=class_date.strftime("%d de %B de %Y"),
        audio_name=audio_name,
        language=language,
        duration=duration_minutes,
        table=segments_to_markdown(segments),
    )

    paths.note_path.write_text(note_content, encoding="utf-8")
    paths.transcript_path.write_text(transcript_content, encoding="utf-8")


def _list_to_markdown(items: Iterable[str]) -> str:
    items = list(item.strip() for item in items if item and item.strip())
    if not items:
        return "- (Sin información registrada)"
    return "\n".join(f"- {item}" for item in items)
