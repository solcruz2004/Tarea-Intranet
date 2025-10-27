"""Cargar configuración desde variables de entorno."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Configuración de la aplicación."""

    lm_studio_base_url: str
    lm_studio_model: str
    whisper_model_size: str
    whisper_compute_type: str
    whisper_language: Optional[str]
    notes_root: Path


def get_settings() -> Settings:
    """Obtiene la configuración desde las variables de entorno."""

    base_url = _get_env("LM_STUDIO_BASE_URL", "http://host.docker.internal:1234/v1")
    model = _get_env("LM_STUDIO_MODEL", "Meta-Llama-3-8B-Instruct")
    whisper_model = _get_env("WHISPER_MODEL_SIZE", "small")
    compute_type = _get_env("WHISPER_COMPUTE_TYPE", "auto")
    language = _get_env("WHISPER_LANGUAGE", "").strip() or None
    notes_root = Path(_get_env("NOTES_ROOT", "data/notes")).expanduser()
    notes_root = Path(_get_env("NOTES_ROOT", "/app/notes")).expanduser()

    return Settings(
        lm_studio_base_url=base_url.rstrip("/"),
        lm_studio_model=model,
        whisper_model_size=whisper_model,
        whisper_compute_type=compute_type,
        whisper_language=language,
        notes_root=notes_root,
    )


def _get_env(name: str, default: str) -> str:
    import os

    return os.getenv(name, default)
