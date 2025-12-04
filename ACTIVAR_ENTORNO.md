# 🔧 Cómo Activar el Entorno Virtual

## ✅ Entorno Virtual Configurado

El proyecto ya tiene un entorno virtual (`venv`) con todas las dependencias instaladas.

## 🚀 Formas de Activar y Ejecutar

### Opción 1: Script Automático (Más Fácil)

**Windows (CMD):**
```cmd
iniciar_servidor.bat
```

**Windows (PowerShell):**
```powershell
.\iniciar_servidor.ps1
```

Estos scripts activan automáticamente el entorno virtual e inician el servidor.

### Opción 2: Manual

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
python manage.py runserver
```

**Linux/Mac:**
```bash
source venv/bin/activate
python manage.py runserver
```

## 🔍 Verificar que el Entorno Virtual Está Activo

Cuando el entorno virtual está activo, verás `(venv)` al inicio de la línea de comandos:

```
(venv) PS C:\...\APE 4>
```

## ⚠️ Si Tienes Problemas con PowerShell

Si PowerShell no permite ejecutar scripts, ejecuta esto primero:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📝 Comandos Útiles

### Activar entorno virtual:
```powershell
.\venv\Scripts\Activate.ps1
```

### Desactivar entorno virtual:
```powershell
deactivate
```

### Verificar que Django funciona:
```powershell
python manage.py check
```

### Iniciar servidor:
```powershell
python manage.py runserver
```

### Instalar nuevas dependencias:
```powershell
pip install nombre_paquete
```

## 🎯 Estado Actual

✅ Entorno virtual creado  
✅ Todas las dependencias instaladas  
✅ Django configurado  
✅ Listo para ejecutar  

## 🚀 Inicio Rápido

1. Abre PowerShell o CMD en la carpeta `APE 4`
2. Ejecuta: `.\iniciar_servidor.ps1` (PowerShell) o `iniciar_servidor.bat` (CMD)
3. Abre tu navegador en: http://localhost:8000

¡Listo! 🎉

