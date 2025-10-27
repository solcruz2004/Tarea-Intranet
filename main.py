from __future__ import annotations

import sys


def _launch_gui() -> None:
    from app.gui import launch_gui

    launch_gui()


def _launch_cli() -> None:
    from app.cli import main as cli_main

    cli_main()


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or "--gui" in args:
        if "--gui" in args:
            args.remove("--gui")
            sys.argv = [sys.argv[0], *args]
        _launch_gui()
    else:
        _launch_cli()
