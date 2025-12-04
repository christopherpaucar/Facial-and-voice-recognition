# 🚀 Inicio Rápido - Sistema de Reconocimiento de Rostros

## ⚡ Iniciar el Servidor (3 Pasos)

### Paso 1: Abrir Terminal en la Carpeta Correcta

**Importante**: Debes estar en la carpeta `APE 4` del proyecto.

**Opción A: Desde el Explorador de Archivos**
1. Navega a: `C:\Users\Usuario\OneDrive - UNIVERSIDAD TÉCNICA DE AMBATO\Escritorio\Séptimo\IA\APES\APE 4`
2. Haz clic derecho en la carpeta
3. Selecciona "Abrir en Terminal" o "Abrir PowerShell aquí"

**Opción B: Desde PowerShell**
```powershell
cd "C:\Users\Usuario\OneDrive - UNIVERSIDAD TÉCNICA DE AMBATO\Escritorio\Séptimo\IA\APES\APE 4"
```

### Paso 2: Activar Entorno Virtual

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Si tienes error de ejecución de scripts:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego intenta de nuevo:
```powershell
.\venv\Scripts\Activate.ps1
```

**CMD (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

### Paso 3: Iniciar Servidor

```powershell
python manage.py runserver
```

## ✅ Verificar que Funciona

Deberías ver algo como:
```
System check identified no issues (0 silenced).
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## 🌐 Acceder a la Aplicación

Abre tu navegador y visita:
- **http://localhost:8000/**
- **http://127.0.0.1:8000/**

## 📋 Comandos Completos (Copia y Pega)

**PowerShell (una sola línea):**
```powershell
cd "C:\Users\Usuario\OneDrive - UNIVERSIDAD TÉCNICA DE AMBATO\Escritorio\Séptimo\IA\APES\APE 4"; .\venv\Scripts\Activate.ps1; python manage.py runserver
```

**O usa el script automático:**
```powershell
cd "C:\Users\Usuario\OneDrive - UNIVERSIDAD TÉCNICA DE AMBATO\Escritorio\Séptimo\IA\APES\APE 4"
.\iniciar_servidor.ps1
```

## 🔍 Verificar Directorio Actual

Para saber en qué carpeta estás:
```powershell
pwd
```

O:
```powershell
Get-Location
```

## ⚠️ Problemas Comunes

### Error: "No se reconoce como cmdlet"
**Causa**: No estás en la carpeta correcta del proyecto.

**Solución**: 
```powershell
cd "C:\Users\Usuario\OneDrive - UNIVERSIDAD TÉCNICA DE AMBATO\Escritorio\Séptimo\IA\APES\APE 4"
```

### Error: "No se puede cargar porque la ejecución de scripts está deshabilitada"
**Solución**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "No module named 'django'"
**Causa**: El entorno virtual no está activado.

**Solución**: Activa el entorno virtual primero:
```powershell
.\venv\Scripts\Activate.ps1
```

## 🎯 Ruta Completa del Proyecto

```
C:\Users\Usuario\OneDrive - UNIVERSIDAD TÉCNICA DE AMBATO\Escritorio\Séptimo\IA\APES\APE 4
```

## 💡 Tip: Crear Acceso Directo

Puedes crear un acceso directo al script `iniciar_servidor.ps1` en tu escritorio para iniciar el servidor con un doble clic.

---

**¡Listo para usar!** 🚀

