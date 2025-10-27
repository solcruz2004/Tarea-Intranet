"""Cargar configuración desde variables de entorno."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import sys

from dotenv import load_dotenv

from .paths import APP_ROOT, resolve_app_path


def _load_dotenv() -> None:
    """Carga el archivo .env tomando en cuenta la ruta del ejecutable."""

    env_path = APP_ROOT / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()


_load_dotenv()


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

    default_base_url = "http://127.0.0.1:1234/v1"
    base_url = _get_env("LM_STUDIO_BASE_URL", default_base_url)
    model = _get_env("LM_STUDIO_MODEL", "Meta-Llama-3-8B-Instruct")
    whisper_model = _get_env("WHISPER_MODEL_SIZE", "small")
    compute_type = _get_env("WHISPER_COMPUTE_TYPE", "auto")
    language = _get_env("WHISPER_LANGUAGE", "").strip() or None
    if getattr(sys, "frozen", False):
        default_notes_root = "notes"
    else:
        default_notes_root = "data/notes"

    notes_root_raw = _get_env("NOTES_ROOT", default_notes_root)
    notes_root = Path(notes_root_raw).expanduser()
    if not notes_root.is_absolute():
        notes_root = resolve_app_path(notes_root_raw)

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
