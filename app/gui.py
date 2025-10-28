"""Interfaz gráfica sencilla para la automatización."""

from __future__ import annotations

import logging
import os
import sys
import threading
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Optional

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkbootstrap import Style

from .config import get_settings
from .services import ServiceManager, ServiceStatus
from typing import Optional

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .config import get_settings
from .workflow import WorkflowResult, run_workflow


class TextWidgetHandler(logging.Handler):
    """Envía los mensajes de logging a un widget de texto."""

    def __init__(self, widget: tk.Text) -> None:
        super().__init__()
        self.widget = widget

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.widget.after(0, self._append, msg)

    def _append(self, message: str) -> None:
        self.widget.configure(state=tk.NORMAL)
        self.widget.insert(tk.END, message + "\n")
        self.widget.configure(state=tk.DISABLED)
        self.widget.see(tk.END)


class NotesApp:
    """Aplicación principal de la interfaz gráfica."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.service_manager = ServiceManager(self.settings)
        self.style = Style(theme=self.settings.gui_theme)
        self.root = self.style.master
        self.root.title("Cuaderno automático de clases")
        self.root.geometry("960x640")
        self.root.minsize(920, 620)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root = tk.Tk()
        self.root.title("Cuaderno automático de clases")
        self.root.geometry("720x520")
        self.root.resizable(False, False)

        self.audio_path_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.notes_root_var = tk.StringVar(value=str(self.settings.notes_root))
        self.skip_summary_var = tk.BooleanVar(value=False)

        self.progress: Optional[ttk.Progressbar] = None
        self.log_text: Optional[tk.Text] = None
        self.run_button: Optional[ttk.Button] = None
        self.service_vars: Dict[str, tk.StringVar] = {}
        self.service_labels: Dict[str, ttk.Label] = {}

        self._build_ui()
        self._configure_logging()
        self._start_service_checks()

        self._build_ui()
        self._configure_logging()

    def run(self) -> None:
        self.root.mainloop()

    # ------------------------------------------------------------------
    # Construcción de UI
    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        main_frame = ttk.Frame(self.root, padding=24)
        main_frame.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 16))
        ttk.Label(
            header,
            text="Asistente automático de apuntes",
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor=tk.W)
        ttk.Label(
            header,
            text="Carga un audio y deja que el asistente sincronice LM Studio, Docker y Obsidian por ti.",
            font=("Segoe UI", 11),
        ).pack(anchor=tk.W, pady=(6, 0))

        content = ttk.Frame(main_frame)
        content.pack(fill=tk.BOTH, expand=True)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)

        form_card = ttk.Labelframe(
            content,
            text="1. Selecciona tu clase",
            padding=20,
            bootstyle="primary",
        )
        form_card.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 18))
        form_card.columnconfigure(1, weight=1)

        self._add_file_selector(form_card, "Archivo de audio", self.audio_path_var, 0)
        self._add_entry(form_card, "Título de la clase", self.title_var, 1)
        self._add_entry(form_card, "Fecha (YYYY-MM-DD)", self.date_var, 2)
        self._add_folder_selector(form_card, "Cuaderno de notas", self.notes_root_var, 3)

        checkbox = ttk.Checkbutton(
            form_card,
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        form = ttk.Frame(main_frame)
        form.pack(fill=tk.X, pady=(0, 20))

        self._add_file_selector(form, "Archivo de audio", self.audio_path_var, 0)
        self._add_entry(form, "Título de la clase", self.title_var, 1)
        self._add_entry(form, "Fecha (YYYY-MM-DD)", self.date_var, 2)
        self._add_folder_selector(form, "Carpeta de notas", self.notes_root_var, 3)

        checkbox = ttk.Checkbutton(
            form,
            text="Omitir resumen (solo guardar transcripción)",
            variable=self.skip_summary_var,
        )
        checkbox.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))

        status_card = ttk.Labelframe(
            content,
            text="2. Verificación del entorno",
            padding=20,
            bootstyle="info",
        )
        status_card.grid(row=0, column=1, sticky=tk.NSEW)
        status_card.columnconfigure(0, weight=1)
        self._build_status_panel(status_card)

        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=16)
        self.run_button = ttk.Button(
            action_frame,
            text="Generar apuntes automáticos",
            bootstyle="success",
        self.run_button = ttk.Button(
            main_frame,
            text="Generar apuntes",
            command=self._on_run_clicked,
        )
        self.run_button.pack(fill=tk.X)

        self.progress = ttk.Progressbar(action_frame, mode="indeterminate", bootstyle="info-striped")
        self.progress.pack(fill=tk.X, pady=(12, 0))

        log_card = ttk.Labelframe(main_frame, text="Registro de actividad", padding=12)
        log_card.pack(fill=tk.BOTH, expand=True)
        self.log_text = tk.Text(
            log_card,
            height=12,
            state=tk.DISABLED,
            relief=tk.FLAT,
            background=self.style.colors.input,
            foreground=self.style.colors.fg,
        )
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=12)

        ttk.Label(main_frame, text="Registro de actividad:").pack(anchor=tk.W)
        self.log_text = tk.Text(main_frame, height=16, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def _add_entry(self, parent: ttk.Frame, label: str, variable: tk.StringVar, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=6)
        entry = ttk.Entry(parent, textvariable=variable)
        entry.grid(row=row, column=1, sticky=tk.EW, pady=6)
        entry = ttk.Entry(parent, textvariable=variable, width=58)
        entry.grid(row=row, column=1, sticky=tk.W, pady=6)

    def _add_file_selector(
        self, parent: ttk.Frame, label: str, variable: tk.StringVar, row: int
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=6)
        entry = ttk.Entry(parent, textvariable=variable)
        entry.grid(row=row, column=1, sticky=tk.EW, pady=6)
        entry = ttk.Entry(parent, textvariable=variable, width=58)
        entry.grid(row=row, column=1, sticky=tk.W, pady=6)
        ttk.Button(parent, text="Buscar", command=self._select_audio).grid(
            row=row, column=2, padx=(10, 0)
        )

    def _add_folder_selector(
        self, parent: ttk.Frame, label: str, variable: tk.StringVar, row: int
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=6)
        entry = ttk.Entry(parent, textvariable=variable)
        entry.grid(row=row, column=1, sticky=tk.EW, pady=6)
        entry = ttk.Entry(parent, textvariable=variable, width=58)
        entry.grid(row=row, column=1, sticky=tk.W, pady=6)
        ttk.Button(parent, text="Elegir carpeta", command=self._select_folder).grid(
            row=row, column=2, padx=(10, 0)
        )

    # ------------------------------------------------------------------
    # Lógica de interacción
    # ------------------------------------------------------------------
    def _select_audio(self) -> None:
        initial_dir = Path(self.audio_path_var.get()).parent if self.audio_path_var.get() else Path.cwd()
        file_path = filedialog.askopenfilename(
            title="Selecciona tu clase",
            filetypes=[
                ("Audio", "*.mp3 *.wav *.m4a *.aac *.ogg *.flac"),
                ("Todos los archivos", "*.*"),
            ],
            initialdir=initial_dir,
        )
        if file_path:
            self.audio_path_var.set(file_path)
            if not self.title_var.get().strip():
                self.title_var.set(Path(file_path).stem.replace("_", " ").title())

    def _select_folder(self) -> None:
        initial_dir = self.notes_root_var.get() or str(Path.cwd())
        folder = filedialog.askdirectory(title="Selecciona dónde guardar las notas", initialdir=initial_dir)
        if folder:
            self.notes_root_var.set(folder)

    def _on_run_clicked(self) -> None:
        if self.run_button is None or self.progress is None:
            return

        audio_path = Path(self.audio_path_var.get().strip())
        if not audio_path.exists():
            messagebox.showerror("Archivo no encontrado", "Selecciona un archivo de audio válido.")
            return

        try:
            class_date = self._parse_date(self.date_var.get().strip())
        except ValueError:
            messagebox.showerror(
                "Fecha inválida", "La fecha debe tener el formato YYYY-MM-DD (por ejemplo 2024-05-20)."
            )
            return

        notes_root = Path(self.notes_root_var.get().strip()) if self.notes_root_var.get().strip() else None
        title = self.title_var.get().strip() or audio_path.stem
        skip_summary = self.skip_summary_var.get()

        self._clear_log()
        logging.info("Iniciando proceso para %s", audio_path.name)

        self._set_processing_state(True)
        thread = threading.Thread(
            target=self._execute_workflow,
            args=(audio_path, title, class_date, notes_root, skip_summary),
            daemon=True,
        )
        thread.start()

    def _execute_workflow(
        self,
        audio_path: Path,
        title: str,
        class_date: date,
        notes_root: Optional[Path],
        skip_summary: bool,
    ) -> None:
        try:
            result = run_workflow(
                audio_path=audio_path,
                title=title,
                class_date=class_date,
                notes_root=notes_root,
                skip_summary=skip_summary,
            )
        except Exception as exc:  # pragma: no cover - mostrado en la UI
            logging.exception("No se pudo completar el proceso")
            self.root.after(0, lambda: self._show_error(str(exc)))
        else:
            self.root.after(0, lambda: self._show_success(result))
        finally:
            self.root.after(0, lambda: self._set_processing_state(False))

    def _show_success(self, result: WorkflowResult) -> None:
        obsidian_opened = False
        if self.settings.auto_launch_obsidian:
            obsidian_opened = self.service_manager.open_obsidian()

        message = (
            "¡Proceso finalizado!\n\n"
            f"Notas: {result.note_path}\n"
            f"Transcripción completa: {result.transcript_path}\n\n"
        )
        if obsidian_opened:
            message += "Obsidian se abrió con tu cuaderno."
        else:
            message += "Abre tu cuaderno en Obsidian para complementar los apuntes."
            "Puedes abrir la carpeta de notas en Obsidian para revisar y complementar tus apuntes."
        )
        messagebox.showinfo("Automatización completada", message)
        self._open_folder(result.note_path.parent)

    def _show_error(self, message: str) -> None:
        messagebox.showerror("Ocurrió un problema", message)

    def _set_processing_state(self, processing: bool) -> None:
        if self.run_button is None or self.progress is None:
            return

        if processing:
            self.run_button.configure(state=tk.DISABLED, text="Trabajando...")
            self.progress.start(10)
        else:
            self.run_button.configure(state=tk.NORMAL, text="Generar apuntes")
            self.progress.stop()

    def _configure_logging(self) -> None:
        if self.log_text is None:
            return

        handler = TextWidgetHandler(self.log_text)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%H:%M:%S"))

        root_logger = logging.getLogger()
        for existing in list(root_logger.handlers):
            root_logger.removeHandler(existing)

        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)
        logging.info(
            "Todo listo. Selecciona tu archivo de audio y pulsa 'Generar apuntes' para comenzar."
        )

    def _build_status_panel(self, parent: ttk.Frame) -> None:
        descriptions = {
            "lmstudio": "Motor de lenguaje (LM Studio)",
            "docker": "Contenedores auxiliares",
            "obsidian": "Cuaderno de notas (Obsidian)",
        }
        for row, (key, title) in enumerate(descriptions.items()):
            ttk.Label(parent, text=title, font=("Segoe UI", 10, "bold")).grid(
                row=row * 2,
                column=0,
                sticky=tk.W,
                pady=(0, 2),
            )
            status_var = tk.StringVar(value="Comprobando...")
            label = ttk.Label(parent, textvariable=status_var, wraplength=240, bootstyle="secondary")
            label.grid(row=row * 2 + 1, column=0, sticky=tk.W, pady=(0, 12))
            self.service_vars[key] = status_var
            self.service_labels[key] = label

    def _start_service_checks(self) -> None:
        if not self.settings.auto_bootstrap_services:
            for key in self.service_vars:
                self._update_service_badge(
                    key,
                    "El autoarranque está desactivado. Puedes iniciarlo manualmente desde la configuración.",
                    "warning",
                )
            return

        for key in self.service_vars:
            self._update_service_badge(key, "Comprobando servicios...", "info")

        thread = threading.Thread(target=self._bootstrap_services, daemon=True)
        thread.start()

    def _bootstrap_services(self) -> None:
        def publish(status: ServiceStatus) -> None:
            self.root.after(0, lambda s=status: self._update_service_status(s))

        statuses = self.service_manager.bootstrap_services(callback=publish)
        if all(status.ready for status in statuses):
            logging.info("Entorno listo: LM Studio, Docker y Obsidian están sincronizados.")
        else:
            logging.warning(
                "Algunos servicios no pudieron iniciarse automáticamente. Revisa la sección 'Verificación del entorno'."
            )

    def _update_service_status(self, status: ServiceStatus) -> None:
        style = "success" if status.ready else "danger"
        self._update_service_badge(status.key, status.detail, style)

    def _update_service_badge(self, key: str, detail: str, style: str) -> None:
        var = self.service_vars.get(key)
        label = self.service_labels.get(key)
        if not var or not label:
            return
        var.set(detail)
        label.configure(bootstyle=style)

    def _clear_log(self) -> None:
        if self.log_text is None:
            return

        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _on_close(self) -> None:
        self.service_manager.shutdown()
        self.root.destroy()

    @staticmethod
    def _parse_date(value: str) -> date:
        return datetime.strptime(value, "%Y-%m-%d").date()

    @staticmethod
    def _open_folder(path: Path) -> None:
        try:
            if os.name == "nt":
                os.startfile(path)  # type: ignore[attr-defined]
            elif os.name == "posix":
                import subprocess

                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.Popen([opener, str(path)])
        except Exception:
            # Si no se puede abrir automáticamente, no interrumpimos el flujo.
            logging.info("Abre manualmente la carpeta: %s", path)


def launch_gui() -> None:
    """Arranca la aplicación gráfica."""

    app = NotesApp()
    app.run()
