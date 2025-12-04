# 📦 Guía de Instalación

## ⚠️ Error: "No module named 'django'"

Si ves este error al ejecutar `python manage.py`, significa que Django y las demás dependencias no están instaladas.

## ✅ Solución: Instalar Dependencias

### Opción 1: Instalación Directa (Recomendado para empezar rápido)

```bash
cd "APE 4"
pip install -r requirements.txt
```

### Opción 2: Usar Entorno Virtual (Recomendado para producción)

1. **Crear entorno virtual:**
```bash
cd "APE 4"
python -m venv venv
```

2. **Activar entorno virtual:**
   - **Windows (PowerShell):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   - **Windows (CMD):**
   ```cmd
   venv\Scripts\activate.bat
   ```
   - **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## 🔍 Verificar Instalación

Después de instalar, verifica que todo funcione:

```bash
python manage.py check
```

Si todo está bien, deberías ver:
```
System check identified no issues (0 silenced).
```

## 📋 Dependencias Principales

- Django 5.0.6
- opencv-python 4.9.0.80
- numpy 1.26.4
- scikit-learn 1.4.0
- tensorflow 2.15.0
- joblib 1.3.2
- Pillow 10.2.0
- matplotlib 3.8.2

## 🚀 Siguiente Paso

Una vez instaladas las dependencias, continúa con:

```bash
python manage.py migrate
python manage.py runserver
```

