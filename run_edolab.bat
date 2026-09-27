@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" goto missing_python

.venv\Scripts\python.exe --version >nul 2>&1
if errorlevel 1 goto broken_python

.venv\Scripts\python.exe -c "import streamlit, plotly" >nul 2>&1
if errorlevel 1 goto missing_dependencies

.venv\Scripts\python.exe -m streamlit run app.py
goto end

:missing_python
echo No se encontro el interprete del entorno .venv.
echo Instala Python 3.12 y sigue los pasos de reparacion indicados en README.md.
goto end

:broken_python
echo El entorno .venv apunta a una instalacion base de Python que no esta disponible.
echo Revisa .venv\pyvenv.cfg y reconstruye .venv con una instalacion funcional de Python 3.12.
goto end

:missing_dependencies
echo Python funciona, pero faltan dependencias de la aplicacion.
echo Ejecuta: .venv\Scripts\python.exe -m pip install -r requirements.txt
goto end

:end
pause
