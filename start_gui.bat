@echo off
cd /d "%~dp0"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py --gui
pause
