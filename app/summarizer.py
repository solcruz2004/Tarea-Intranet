"""Generación de resúmenes estructurados mediante LM Studio."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Dict, List

import requests

logger = logging.getLogger(__name__)


@dataclass
class Summary:
    """Estructura de los datos sintetizados por el LLM."""

    avance_clase: List[str]
    tareas: List[str]
    pendientes: List[str]
    preguntas_examen: List[str]


class SummarizationError(RuntimeError):
    """Se lanza cuando no se puede generar el resumen."""


SYSTEM_PROMPT = (
    "Eres un asistente pedagógico que ayuda a tomar apuntes de clases. "
    "Analiza la transcripción literal y crea elementos accionables claros." 
    "Responde exclusivamente en formato JSON válido con las claves: "
    "'avance_clase', 'tareas', 'pendientes', 'preguntas_examen'. Cada clave "
    "debe mapear a una lista de strings concretos y accionables."
)


USER_TEMPLATE = """
Transcripción de la clase:
"""
{transcript}
"""

Fecha de la clase: {class_date}
Título o asignatura: {class_title}

Devuelve un JSON con los aprendizajes, las tareas, los pendientes y posibles preguntas de examen.
"""


def build_prompt(transcript: str, class_date: str, class_title: str) -> str:
    return USER_TEMPLATE.format(transcript=transcript.strip(), class_date=class_date, class_title=class_title)


def call_lm_studio(
    base_url: str,
    model: str,
    transcript: str,
    class_date: str,
    class_title: str,
    temperature: float = 0.2,
) -> Summary:
    """Invoca el endpoint OpenAI-compatible de LM Studio."""

    prompt = build_prompt(transcript, class_date, class_title)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": 800,
    }

    url = f"{base_url}/chat/completions"
    logger.info("Solicitando resumen a LM Studio en %s", url)
    response = requests.post(url, json=payload, timeout=120)

    if response.status_code != 200:
        raise SummarizationError(f"Error {response.status_code}: {response.text}")

    content = response.json()["choices"][0]["message"]["content"].strip()

    try:
        data: Dict[str, List[str]] = json.loads(content)
    except json.JSONDecodeError as exc:
        logger.error("No se pudo interpretar la respuesta JSON: %s", content)
        raise SummarizationError("La respuesta del modelo no es JSON válido") from exc

    return Summary(
        avance_clase=data.get("avance_clase", []),
        tareas=data.get("tareas", []),
        pendientes=data.get("pendientes", []),
        preguntas_examen=data.get("preguntas_examen", []),
    )
