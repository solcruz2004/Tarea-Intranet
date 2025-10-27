"""Utilidades de rutas compatibles con ejecución empaquetada."""

from __future__ import annotations

from pathlib import Path
import sys


def get_app_root() -> Path:
    """Devuelve la carpeta base donde residen los recursos del proyecto.

    Cuando la aplicación se ejecuta empaquetada con PyInstaller (``sys.frozen``)
    la ruta corresponde al directorio del ejecutable. En modo desarrollo se
    utiliza la carpeta raíz del repositorio.
    """

    if getattr(sys, "frozen", False) and hasattr(sys, "executable"):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


APP_ROOT = get_app_root()


def resolve_app_path(relative: str) -> Path:
    """Convierte rutas relativas al directorio base de la aplicación."""

    path = Path(relative)
    if path.is_absolute():
        return path
    return (APP_ROOT / path).resolve()
