# Script PowerShell para iniciar el servidor Django
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Sistema de Reconocimiento de Rostros" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Verificando configuracion..." -ForegroundColor Yellow
python manage.py check

Write-Host ""
Write-Host "Iniciando servidor Django..." -ForegroundColor Green
Write-Host ""
Write-Host "El servidor estara disponible en: http://localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver

