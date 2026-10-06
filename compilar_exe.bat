@echo off
setlocal
pushd "%~dp0"
set PY=python
where python >nul 2>nul || set PY=py
where %PY% >nul 2>nul || (echo Instala Python 3 desde python.org y marca "Add Python to PATH".& pause & exit /b 1)
%PY% -m pip install --upgrade pyinstaller
%PY% -m PyInstaller --onefile --name WE9_WE9LE_convertidor we9_we9le.py
echo.
echo Listo: el .exe portable esta en la carpeta "dist".
pause
