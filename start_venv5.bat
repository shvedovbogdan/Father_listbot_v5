@echo off
setlocal EnableExtensions

REM ===== User settings =====
set "VENV_NAME=venv5"
set "PYTHON_EXE=python"
set "ENTRYPOINT=main.py"
set "RECREATE_VENV=0"
REM =========================

cd /d "%~dp0"

if not exist "%ENTRYPOINT%" (
    if exist "father_listbot_ready\%ENTRYPOINT%" (
        cd /d "%~dp0father_listbot_ready"
    )
)

echo =====================================
echo Father List Bot Launcher
echo VENV: %VENV_NAME%
echo FILE: %ENTRYPOINT%
echo =====================================
echo.

where %PYTHON_EXE% >nul 2>nul
if errorlevel 1 goto no_python

if "%RECREATE_VENV%"=="1" (
    if exist "%VENV_NAME%" (
        echo Removing old virtual environment...
        rmdir /s /q "%VENV_NAME%"
    )
)

if not exist "%ENTRYPOINT%" goto no_entry

if not exist "%VENV_NAME%\Scripts\python.exe" (
    echo Creating virtual environment "%VENV_NAME%"...
    %PYTHON_EXE% -m venv "%VENV_NAME%"
    if errorlevel 1 goto venv_fail
)

call "%VENV_NAME%\Scripts\activate.bat"
if errorlevel 1 goto activate_fail

echo Upgrading pip...
python -m pip install --upgrade pip --disable-pip-version-check
if errorlevel 1 goto pip_fail

echo Installing project dependencies...
if exist requirements.txt (
    python -m pip install --upgrade --force-reinstall -r requirements.txt --disable-pip-version-check
) else (
    echo requirements.txt not found. Installing fallback packages...
    python -m pip install --upgrade --force-reinstall aiogram==2.25.1 aiohttp==3.8.6 python-dotenv==1.1.1 pytz==2025.2 --disable-pip-version-check
)
if errorlevel 1 goto deps_fail

echo Checking aiogram version...
python -c "import aiogram; print(aiogram.__version__)"
if errorlevel 1 goto deps_fail

if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env from .env.example ...
        copy /y ".env.example" ".env" >nul
        echo EDIT .env AND SET BOT_TOKEN AND ADMIN_IDS BEFORE FIRST REAL RUN.
    )
)

echo.
echo Starting bot...
python "%ENTRYPOINT%"
echo.
pause
exit /b 0

:no_python
echo [ERROR] Python was not found in PATH.
echo Install Python 3.10+ and enable "Add Python to PATH".
pause
exit /b 1

:no_entry
echo [ERROR] "%ENTRYPOINT%" was not found.
echo Put this BAT file in the bot folder with main.py.
pause
exit /b 1

:venv_fail
echo [ERROR] Failed to create virtual environment.
pause
exit /b 1

:activate_fail
echo [ERROR] Failed to activate "%VENV_NAME%".
pause
exit /b 1

:pip_fail
echo [ERROR] Failed to upgrade pip.
pause
exit /b 1

:deps_fail
echo [ERROR] Failed to install dependencies.
echo Try deleting the folder "%VENV_NAME%" and run this BAT again.
pause
exit /b 1
