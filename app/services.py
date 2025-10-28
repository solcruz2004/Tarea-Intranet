"""Gestión automática de servicios auxiliares (LM Studio, Docker y Obsidian)."""
from __future__ import annotations

import logging
import os
import shlex
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional

import requests

from .config import Settings

logger = logging.getLogger(__name__)


@dataclass
class ServiceStatus:
    """Representa el resultado de comprobar o iniciar un servicio."""

    key: str
    title: str
    detail: str
    ready: bool


class ServiceManager:
    """Se encarga de verificar y lanzar los servicios auxiliares."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._started_processes: List[subprocess.Popen[bytes]] = []
        self._compose_command: Optional[List[str]] = self._resolve_compose_command()
        self._obsidian_launched = False

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------
    def bootstrap_services(
        self,
        auto_start: Optional[bool] = None,
        callback: Optional[Callable[[ServiceStatus], None]] = None,
    ) -> List[ServiceStatus]:
        """Verifica e inicia todos los servicios necesarios.

        Args:
            auto_start: Si es ``True`` se intentará iniciar servicios caídos.
                Si es ``False`` únicamente se verifican. ``None`` usa el valor
                configurado en ``Settings.auto_bootstrap_services``.
            callback: Función que recibe cada ``ServiceStatus`` generado.
        """

        if auto_start is None:
            auto_start = self.settings.auto_bootstrap_services

        statuses = [
            self._ensure_obsidian(auto_start=auto_start),
            self._ensure_docker(auto_start=auto_start),
            self._ensure_lm_studio(auto_start=auto_start),
        ]

        for status in statuses:
            if callback:
                callback(status)

        return statuses

    def open_obsidian(self) -> bool:
        """Abre el vault de Obsidian si se configuró el ejecutable."""

        executable = self.settings.obsidian_executable
        if executable is None or not executable.exists():
            return False

        vault = self.settings.obsidian_vault

        try:
            command = [str(executable), str(vault)]
            subprocess.Popen(command, cwd=str(executable.parent))
        except Exception as exc:  # pragma: no cover - interacción del SO
            logger.error("No se pudo abrir Obsidian automáticamente: %s", exc)
            return False

        self._obsidian_launched = True
        return True

    def shutdown(self) -> None:
        """Detiene procesos lanzados explícitamente por la aplicación."""

        for process in list(self._started_processes):
            if process.poll() is None:
                try:
                    process.terminate()
                except Exception:
                    pass
        self._started_processes.clear()

    # ------------------------------------------------------------------
    # Comprobaciones
    # ------------------------------------------------------------------
    def _ensure_obsidian(self, auto_start: bool) -> ServiceStatus:
        vault = self.settings.obsidian_vault
        vault.mkdir(parents=True, exist_ok=True)

        detail = f"Vault preparado en {vault}"
        ready = True

        if auto_start and self.settings.auto_launch_obsidian and not self._obsidian_launched:
            if self.open_obsidian():
                detail += " · Obsidian iniciado"
            else:
                detail += " · Abre Obsidian manualmente si deseas visualizar las notas"

        return ServiceStatus(
            key="obsidian",
            title="Obsidian",
            detail=detail,
            ready=ready,
        )

    def _ensure_docker(self, auto_start: bool) -> ServiceStatus:
        compose_file = self.settings.docker_compose_file
        if compose_file is None:
            return ServiceStatus(
                key="docker",
                title="Contenedores",
                detail="No se configuró docker-compose; se omite este paso.",
                ready=True,
            )

        if not compose_file.exists():
            return ServiceStatus(
                key="docker",
                title="Contenedores",
                detail=f"No se encontró el archivo {compose_file}.",
                ready=False,
            )

        if self._compose_command is None:
            return ServiceStatus(
                key="docker",
                title="Contenedores",
                detail="Docker CLI no está disponible en esta máquina.",
                ready=False,
            )

        if self._containers_running(compose_file):
            return ServiceStatus(
                key="docker",
                title="Contenedores",
                detail="Servicios en Docker activos y listos.",
                ready=True,
            )

        if not auto_start:
            return ServiceStatus(
                key="docker",
                title="Contenedores",
                detail="Los contenedores no están activos. Inícialos manualmente con docker compose up -d.",
                ready=False,
            )

        if not self._compose_up(compose_file):
            return ServiceStatus(
                key="docker",
                title="Contenedores",
                detail="No se pudieron iniciar los contenedores automáticamente.",
                ready=False,
            )

        if self._wait_for(lambda: self._containers_running(compose_file)):
            return ServiceStatus(
                key="docker",
                title="Contenedores",
                detail="Contenedores levantados y ejecutándose.",
                ready=True,
            )

        return ServiceStatus(
            key="docker",
            title="Contenedores",
            detail="Docker respondió pero los servicios no alcanzaron el estado 'running'.",
            ready=False,
        )

    def _ensure_lm_studio(self, auto_start: bool) -> ServiceStatus:
        if self._lm_studio_ready():
            return ServiceStatus(
                key="lmstudio",
                title="LM Studio",
                detail=f"Conectado a {self.settings.lm_studio_base_url}.",
                ready=True,
            )

        if not auto_start:
            return ServiceStatus(
                key="lmstudio",
                title="LM Studio",
                detail="LM Studio no responde. Verifica que el servidor esté en ejecución.",
                ready=False,
            )

        command = self.settings.lm_studio_start_command
        if not command:
            return ServiceStatus(
                key="lmstudio",
                title="LM Studio",
                detail="LM Studio no responde y no se configuró LM_STUDIO_START_COMMAND.",
                ready=False,
            )

        process = self._spawn_command(command, cwd=self.settings.lm_studio_workdir)
        if process is None:
            return ServiceStatus(
                key="lmstudio",
                title="LM Studio",
                detail="No se pudo lanzar el comando de LM Studio.",
                ready=False,
            )

        if self._wait_for(self._lm_studio_ready):
            return ServiceStatus(
                key="lmstudio",
                title="LM Studio",
                detail="Servidor de LM Studio iniciado y disponible.",
                ready=True,
            )

        return ServiceStatus(
            key="lmstudio",
            title="LM Studio",
            detail="LM Studio se lanzó pero no respondió a tiempo.",
            ready=False,
        )

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------
    def _lm_studio_ready(self) -> bool:
        try:
            response = requests.get(
                f"{self.settings.lm_studio_base_url}/models",
                timeout=5,
            )
        except requests.RequestException:
            return False
        return response.status_code == 200

    def _spawn_command(self, command: str, cwd: Optional[Path]) -> Optional[subprocess.Popen[bytes]]:
        try:
            args = shlex.split(command, posix=os.name != "nt")
            process = subprocess.Popen(args, cwd=str(cwd) if cwd else None)
        except FileNotFoundError:
            logger.error("No se encontró el ejecutable para el comando: %s", command)
            return None
        except Exception as exc:
            logger.error("No se pudo lanzar el comando '%s': %s", command, exc)
            return None

        self._started_processes.append(process)
        return process

    def _resolve_compose_command(self) -> Optional[List[str]]:
        if self.settings.docker_compose_command:
            return shlex.split(self.settings.docker_compose_command, posix=os.name != "nt")

        if shutil.which("docker"):
            return ["docker", "compose"]
        if shutil.which("docker-compose"):
            return ["docker-compose"]
        return None

    def _compose_up(self, compose_file: Path) -> bool:
        if self._compose_command is None:
            return False

        command = [*self._compose_command, "-f", str(compose_file), "up", "-d"]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                check=False,
                text=True,
            )
        except Exception as exc:
            logger.error("Error al ejecutar docker compose: %s", exc)
            return False

        if result.returncode != 0:
            logger.error("docker compose devolvió un error: %s", result.stderr.strip())
            return False

        return True

    def _containers_running(self, compose_file: Path) -> bool:
        if self._compose_command is None:
            return False

        command = [*self._compose_command, "-f", str(compose_file), "ps"]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                check=False,
                text=True,
            )
        except Exception:
            return False

        if result.returncode != 0:
            return False

        lines = [line.strip().lower() for line in result.stdout.splitlines() if line.strip()]
        return any("running" in line for line in lines)

    def _wait_for(self, condition: Callable[[], bool]) -> bool:
        timeout = self.settings.bootstrap_timeout_seconds
        deadline = time.time() + timeout
        while time.time() < deadline:
            if condition():
                return True
            time.sleep(2)
        return False


__all__ = ["ServiceManager", "ServiceStatus"]
