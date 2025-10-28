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
    auto_bootstrap_services: bool
    bootstrap_timeout_seconds: int
    docker_compose_file: Optional[Path]
    docker_compose_command: Optional[str]
    lm_studio_start_command: Optional[str]
    lm_studio_workdir: Optional[Path]
    auto_launch_obsidian: bool
    obsidian_vault: Path
    obsidian_executable: Optional[Path]
    gui_theme: str


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

    compose_env = _get_env("DOCKER_COMPOSE_FILE", "").strip()
    if compose_env:
        compose_file = resolve_app_path(compose_env)
    else:
        default_compose = APP_ROOT / "docker-compose.yml"
        compose_file = default_compose if default_compose.exists() else None

    obsidian_vault_raw = _get_env("OBSIDIAN_VAULT", str(notes_root))
    obsidian_vault = Path(obsidian_vault_raw).expanduser()
    if not obsidian_vault.is_absolute():
        obsidian_vault = resolve_app_path(obsidian_vault_raw)

    obsidian_exec_raw = _get_env("OBSIDIAN_EXECUTABLE", "").strip()
    obsidian_executable = resolve_app_path(obsidian_exec_raw) if obsidian_exec_raw else None

    workdir_raw = _get_env("LM_STUDIO_WORKDIR", "").strip()
    lm_studio_workdir = resolve_app_path(workdir_raw) if workdir_raw else None

    return Settings(
        lm_studio_base_url=base_url.rstrip("/"),
        lm_studio_model=model,
        whisper_model_size=whisper_model,
        whisper_compute_type=compute_type,
        whisper_language=language,
        notes_root=notes_root,
        auto_bootstrap_services=_get_bool("AUTO_BOOTSTRAP_SERVICES", True),
        bootstrap_timeout_seconds=_get_int("BOOTSTRAP_TIMEOUT_SECONDS", 90),
        docker_compose_file=compose_file,
        docker_compose_command=_get_env("DOCKER_COMPOSE_COMMAND", "").strip() or None,
        lm_studio_start_command=_get_env("LM_STUDIO_START_COMMAND", "").strip() or None,
        lm_studio_workdir=lm_studio_workdir,
        auto_launch_obsidian=_get_bool("AUTO_OPEN_OBSIDIAN", True),
        obsidian_vault=obsidian_vault,
        obsidian_executable=obsidian_executable,
        gui_theme=_get_env("GUI_THEME", "superhero"),
    )


def _get_env(name: str, default: str) -> str:
    import os

    return os.getenv(name, default)


def _get_bool(name: str, default: bool) -> bool:
    raw = _get_env(name, "true" if default else "false").strip().lower()
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    return default


def _get_int(name: str, default: int) -> int:
    raw = _get_env(name, str(default)).strip()
    try:
        return int(raw)
    except ValueError:
        return default
