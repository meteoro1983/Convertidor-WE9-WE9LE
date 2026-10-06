@echo off
setlocal
set PY=python
where python >nul 2>nul || set PY=py
where %PY% >nul 2>nul || (echo Python no esta instalado. Usa compilar_exe.bat en un equipo con Python, o instala Python 3.& pause & exit /b 1)
%PY% "%~dp0we9_we9le.py" %*
