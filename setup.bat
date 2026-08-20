@echo off
REM Run this ONCE. It creates a local "venv" folder right here
REM and installs yt-dlp into it (not system-wide).

cd /d "%~dp0"

echo Creating virtual environment...
python -m venv venv

echo Installing yt-dlp inside the venv...
venv\Scripts\pip install --upgrade pip
venv\Scripts\pip install yt-dlp

echo.
echo ============================================================
echo Setup mostly done. ONE MANUAL STEP LEFT:
echo.
echo   Download portable ffmpeg (Windows build, "essentials" zip)
echo   from: https://www.gyan.dev/ffmpeg/builds/
echo.
echo   Unzip it, then copy the "bin" folder from inside it
echo   into this folder as:
echo       %~dp0ffmpeg\bin
echo   (so ffmpeg.exe ends up at ffmpeg\bin\ffmpeg.exe)
echo ============================================================
echo.
pause
