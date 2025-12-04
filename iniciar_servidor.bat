@echo off
echo ========================================
echo   Sistema de Reconocimiento de Rostros
echo ========================================
echo.
echo Activando entorno virtual...
call venv\Scripts\activate.bat
echo.
echo Verificando configuracion...
python manage.py check
echo.
echo Iniciando servidor Django...
echo.
echo El servidor estara disponible en: http://localhost:8000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
python manage.py runserver
pause

