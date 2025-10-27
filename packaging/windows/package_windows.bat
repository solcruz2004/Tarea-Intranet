@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem -------------------------------------------------------------
rem 1) Ubicar la carpeta del proyecto
rem -------------------------------------------------------------
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."
pushd "%PROJECT_ROOT%" >nul

rem -------------------------------------------------------------
rem 2) Detectar Python disponible
rem -------------------------------------------------------------
set "PYTHON_CMD="
for %%P in ("py -3.11" "py -3" "python") do (
    if not defined PYTHON_CMD (
        call %%~P -V >nul 2>&1
        if not errorlevel 1 (
            set "PYTHON_CMD=%%~P"
        )
    )
)
if not defined PYTHON_CMD (
    echo [ERROR] No se encontro una instalacion de Python.
    echo Instala Python 3.10+ desde https://www.python.org/downloads/
    echo y asegúrate de marcar "Add Python to PATH".
    popd
    exit /b 1
)

echo.
echo === Usando Python: %PYTHON_CMD%

echo === Creando entorno virtual para la compilacion...
set "BUILD_ENV=.venv-build"
if not exist "%BUILD_ENV%" (
    call %PYTHON_CMD% -m venv "%BUILD_ENV%"
)
call "%BUILD_ENV%\Scripts\activate.bat" >nul

python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt >nul
python -m pip install pyinstaller >nul

echo === Limpiando compilaciones anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

set "APP_NAME=CuadernoAutomatico"
set "ICON_PATH="

echo === Empaquetando ejecutable...
pyinstaller --noconfirm --clean --windowed --name "%APP_NAME%" ^
    --add-data ".env.windows.example;." ^
    --add-data "README.md;." ^
    main.py

if errorlevel 1 (
    echo [ERROR] Fallo la construccion del ejecutable.
    deactivate >nul 2>&1
    popd
    exit /b 1
)

echo === Copiando archivos auxiliares...
copy /Y .env.windows.example dist\%APP_NAME%\plantilla.env >nul
copy /Y packaging\windows\portable-readme.txt dist\%APP_NAME%\LEEME.txt >nul
copy /Y docker-compose.yml dist\%APP_NAME%\docker-compose.yml >nul

if exist packaging\windows\bundled (
    echo === Integrando recursos portables (LM Studio, Obsidian, etc.)...
    xcopy /E /I /Y "packaging\windows\bundled" "dist\%APP_NAME%\bundled" >nul
)

if exist dist\%APP_NAME%\CuadernoAutomatico.exe (
    echo.
    echo === Listo! Encontraras el ejecutable en dist\%APP_NAME%\CuadernoAutomatico.exe
    echo Copia tambien el archivo plantilla.env y personalizalo como .env
    echo antes de distribuir la carpeta.
)

echo.
choice /m "Deseas dejar abierto este terminal" /t 5 /d n >nul
if errorlevel 2 (
    cmd /k
)

deactivate >nul 2>&1
popd
endlocal
