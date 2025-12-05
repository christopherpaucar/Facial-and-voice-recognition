# 🤖 Sistema de Reconocimiento de Rostros Humanos

Sistema on-line de visión por computadora para el reconocimiento de rostros humanos utilizando inteligencia artificial. Desarrollado con Django, PCA, SVM y TensorFlow.

---

## 📋 Tabla de Contenidos

- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación Completa](#-instalación-completa)
  - [Verificación de Requisitos Previos](#1-verificación-de-requisitos-previos)
  - [Instalación desde Cero](#2-instalación-desde-cero)
  - [Instalación con Entorno Virtual Existente](#3-instalación-con-entorno-virtual-existente)
- [Ejecución del Proyecto](#-ejecución-del-proyecto)
- [Uso del Sistema](#-uso-del-sistema)
- [Solución de Problemas](#-solución-de-problemas)
- [Estructura del Proyecto](#️-estructura-del-proyecto)
- [Documentación Técnica](#-documentación-técnica)

---

## 💻 Requisitos del Sistema

### Software Requerido

| Componente | Versión Mínima | Versión Recomendada |
|------------|----------------|---------------------|
| **Python** | 3.8 | 3.10 o superior |
| **pip** | 20.0+ | Última versión |
| **Sistema Operativo** | Windows 10, Linux, macOS | Windows 11, Ubuntu 20.04+, macOS 12+ |
| **Navegador Web** | Chrome 90+, Firefox 88+, Edge 90+ | Últimas versiones |
| **Cámara Web** | Opcional | Recomendada para captura |

### Hardware Recomendado

- **RAM**: Mínimo 4GB (recomendado: 8GB+)
- **Procesador**: Mínimo 2 núcleos (recomendado: 4+ núcleos)
- **Espacio en disco**: Mínimo 2GB libres (recomendado: 5GB+)
- **GPU**: Opcional, pero recomendada para entrenamiento con TensorFlow

---

## 🚀 Instalación Completa

### 1. Verificación de Requisitos Previos

#### Verificar Instalación de Python

**Windows (PowerShell/CMD):**
```powershell
python --version
```

**Linux/Mac:**
```bash
python3 --version
```

✅ **Resultado esperado**: `Python 3.8.x` o superior

❌ **Si no está instalado**: 
- **Windows**: Descarga desde [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt-get install python3 python3-pip` (Ubuntu/Debian)
- **Mac**: `brew install python3` (con Homebrew) o descarga desde python.org

#### Verificar Instalación de pip

```bash
pip --version
```

✅ **Resultado esperado**: `pip 20.0.x` o superior

❌ **Si no está instalado**:
```bash
python -m ensurepip --upgrade
```

#### Verificar Git (Opcional, solo si clonas desde repositorio)

```bash
git --version
```

---

### 2. Instalación desde Cero

Esta sección es para usuarios que **NO tienen el entorno virtual configurado** o están instalando el proyecto por primera vez.

#### Paso 1: Obtener el Proyecto

**Opción A: Clonar desde Repositorio Git**
```bash
git clone https://github.com/christopherpaucar/Facial-and-voice-recognition.git
cd "APE 4"
```

**Opción B: Descargar y Extraer ZIP**
1. Descarga el proyecto como ZIP
2. Extrae el contenido
3. Navega a la carpeta `APE 4`:
   ```bash
   cd "APE 4"
   ```

#### Paso 2: Crear Entorno Virtual

**⚠️ IMPORTANTE**: El uso de un entorno virtual es **altamente recomendado** para evitar conflictos con otros proyectos Python.

**Windows (PowerShell):**
```powershell
python -m venv venv
```

**Si aparece error de ejecución de scripts:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
python -m venv venv
```

**Windows (CMD):**
```cmd
python -m venv venv
```

**Linux/Mac:**
```bash
python3 -m venv venv
```

✅ **Verificación**: Deberías ver una carpeta `venv` creada en el directorio del proyecto.

#### Paso 3: Activar Entorno Virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Si aparece error de política de ejecución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

✅ **Verificación**: Deberías ver `(venv)` al inicio de tu línea de comandos:
```
(venv) PS C:\...\APE 4>
```

#### Paso 4: Actualizar pip

```bash
python -m pip install --upgrade pip
```

✅ **Resultado esperado**: `Successfully installed pip-x.x.x`

#### Paso 5: Instalar Dependencias

```bash
pip install -r requirements.txt
```

⏱️ **Tiempo estimado**: 5-15 minutos (dependiendo de tu conexión a internet)

✅ **Verificación**: Al finalizar, deberías ver:
```
Successfully installed django-x.x.x opencv-python-x.x.x ...
```

**⚠️ Notas importantes:**
- Si tienes **Python 3.13**, las dependencias se instalarán automáticamente con versiones compatibles
- Si aparece un error con TensorFlow, asegúrate de tener Python 3.8-3.11 (TensorFlow puede no soportar Python 3.12+ en algunas versiones)
- Si la instalación falla, intenta instalar las dependencias una por una para identificar el problema

#### Paso 6: Verificar Instalación

```bash
python manage.py check
```

✅ **Resultado esperado**:
```
System check identified no issues (0 silenced).
```

❌ **Si aparece error**: Revisa la sección [Solución de Problemas](#-solución-de-problemas)

#### Paso 7: Configurar Base de Datos

```bash
python manage.py migrate
```

✅ **Resultado esperado**:
```
Operations to perform:
  Apply all migrations: ...
Running migrations:
  Applying ... OK
```

✅ **Verificación**: Deberías ver un archivo `db.sqlite3` creado en el directorio del proyecto.

#### Paso 8: Crear Carpetas del Dataset (Opcional)

Las carpetas se crean automáticamente cuando subes imágenes, pero puedes crearlas manualmente:

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Path "dataset\human" -Force
New-Item -ItemType Directory -Path "dataset\non_human" -Force
```

**Linux/Mac:**
```bash
mkdir -p dataset/human dataset/non_human
```

✅ **Verificación**: Deberías ver las carpetas `dataset/human/` y `dataset/non_human/` creadas.

---

### 3. Instalación con Entorno Virtual Existente

Esta sección es para usuarios que **YA tienen el entorno virtual configurado** (por ejemplo, si clonaron un repositorio que ya incluye `venv`).

#### Paso 1: Navegar al Directorio del Proyecto

```bash
cd "APE 4"
```

#### Paso 2: Activar Entorno Virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

✅ **Verificación**: Deberías ver `(venv)` al inicio de tu línea de comandos.

#### Paso 3: Verificar Dependencias

```bash
python manage.py check
```

**Si aparece `No module named 'django'` o similar:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Paso 4: Verificar Base de Datos

```bash
python manage.py migrate
```

✅ **Si todo está correcto**, puedes proceder a [Ejecución del Proyecto](#-ejecución-del-proyecto).

---

## ⚡ Ejecución del Proyecto

### Método 1: Script Automático (Recomendado - Windows)

**PowerShell:**
```powershell
.\iniciar_servidor.ps1
```

**CMD:**
```cmd
iniciar_servidor.bat
```

✅ **Este script automáticamente:**
1. Activa el entorno virtual
2. Verifica las dependencias
3. Ejecuta las migraciones si es necesario
4. Inicia el servidor Django

### Método 2: Ejecución Manual

#### Paso 1: Activar Entorno Virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### Paso 2: Iniciar el Servidor

```bash
python manage.py runserver
```

✅ **Resultado esperado**:
```
System check identified no issues (0 silenced).
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

#### Paso 3: Acceder a la Aplicación

Abre tu navegador y visita:
- **http://localhost:8000/**
- **http://127.0.0.1:8000/**

#### Paso 4: Detener el Servidor

Presiona **Ctrl + C** (o **Ctrl + Break** en Windows) en la terminal.

---

### 📍 URLs Importantes

Una vez que el servidor esté corriendo:

| Página | URL | Descripción |
|--------|-----|-------------|
| 🏠 **Página Principal** | http://localhost:8000/ | Página de inicio del sistema |
| 📸 **Capturar Imágenes** | http://localhost:8000/capture/ | Captura fotos desde cámara web |
| 📊 **Ver Dataset** | http://localhost:8000/dataset/ | Gestiona y sube imágenes al dataset |
| 🎓 **Entrenar Modelo** | http://localhost:8000/train/ | Entrena los modelos de IA |
| 🔍 **Hacer Predicción** | http://localhost:8000/predict/ | Prueba el modelo con nuevas imágenes |
| 📜 **Ver Historial** | http://localhost:8000/history/ | Historial de predicciones realizadas |

---

## 🎯 Características

- ✅ **Preprocesamiento avanzado**: Conversión a escala de grises, filtros Gaussianos, ecualización de histograma, filtros bilaterales
- ✅ **Detección automática**: Detección de rostros usando Haar Cascade de OpenCV con múltiples configuraciones
- ✅ **Múltiples modelos de IA** (entrenados automáticamente):
  - **PCA + SVM**: Reducción de dimensionalidad con PCA y clasificación con Support Vector Machine
  - **TensorFlow/Keras**: Red neuronal convolucional (CNN) para clasificación
  - **Balanceo de clases**: Ambos modelos usan balanceo automático para datasets desbalanceados
- ✅ **Interfaz web completa**: Interfaz Django moderna y responsive con iconos interactivos
- ✅ **Captura desde cámara**: 
  - Captura automática de múltiples fotos (configurable, por defecto 40)
  - Vista previa en tiempo real con efecto espejo
  - Contador regresivo antes de iniciar captura
  - Reactivación automática de cámara
- ✅ **Gestión de dataset**: 
  - Subida de archivos con drag-and-drop
  - Subida múltiple de imágenes
  - Prevención de sobrescritura (renombrado automático)
- ✅ **Predicción mejorada**:
  - Opción de subir archivo o tomar foto desde la cámara
  - Uso automático de ambos modelos (mejor resultado)
  - Tabla de predicciones recientes con actualización automática
  - Modal para ver imágenes de predicciones
- ✅ **Historial completo**: Registro de predicciones y entrenamientos realizados con visualización de imágenes

---

## 🎓 Uso del Sistema

### 1. Preparar el Dataset

El sistema requiere imágenes en **DOS categorías**:

#### Opción A: Captura desde Cámara (Recomendado)

1. Abre tu navegador y ve a: **http://localhost:8000/capture/**
2. Selecciona la categoría:
   - **"Humano"**: Para capturar rostros humanos
   - **"No Humano"**: Para capturar objetos, animales, paisajes, etc.
3. Haz clic en **"Iniciar Cámara"** (la cámara se activará automáticamente)
4. Configura el número de fotos a capturar (por defecto: 40)
5. Haz clic en **"Iniciar Captura"**
6. Permite el acceso a tu cámara cuando el navegador lo solicite
7. Las fotos se capturarán automáticamente con un contador regresivo de 3 segundos

#### Opción B: Subir Imágenes Manualmente

1. Ve a: **http://localhost:8000/dataset/**
2. Usa los componentes de arrastrar y soltar para subir imágenes:
   - **📤 Subir Imágenes Humanas**: Arrastra o selecciona múltiples imágenes
   - **📤 Subir Imágenes No Humanas**: Arrastra o selecciona múltiples imágenes
   - **Nota**: Los archivos con nombres duplicados se renombrarán automáticamente para evitar sobrescritura

#### Opción C: Colocar Imágenes Directamente

Coloca las imágenes en las carpetas correspondientes:

```
dataset/
├── human/          (imágenes con rostros humanos)
│   ├── imagen1.jpg
│   ├── imagen2.jpg
│   └── ...
└── non_human/      (imágenes sin rostros humanos)
    ├── objeto1.jpg
    ├── animal1.jpg
    └── ...
```

**Recomendaciones**:
- **Mínimo**: 20-30 imágenes de cada categoría
- **Recomendado**: 50+ imágenes de cada categoría
- **Ideal**: 100+ imágenes de cada categoría con ratio 1:1 o máximo 2:1
- **Formatos soportados**: JPG, PNG, JPEG
- **Para humanas**: Asegúrate de que los rostros sean claramente visibles y frontales

📖 **Ver más tips**: Consulta `TIPS_FOTOS.md` para recomendaciones detalladas sobre cómo tomar fotos.

### 2. Entrenar el Modelo

#### Opción A: Interfaz Web (Recomendado)

1. Ve a: **http://localhost:8000/train/**
2. Haz clic en **"🚀 Iniciar Entrenamiento"**
   - **Nota**: Se entrenarán automáticamente **ambos modelos** (PCA+SVM y TensorFlow)
3. Espera a que termine el proceso (puede tardar varios minutos)
   - Verás el progreso en tiempo real con tiempo transcurrido
   - Al finalizar, verás los resultados de ambos modelos con accuracy

**Tiempo estimado de entrenamiento**:
- PCA+SVM: 1-5 minutos (dependiendo del dataset)
- TensorFlow: 5-30 minutos (dependiendo del dataset y hardware)

#### Opción B: Línea de Comandos

```bash
python manage.py train_model
```

### 3. Probar el Modelo

1. Ve a: **http://localhost:8000/predict/**
2. Elige cómo subir la imagen:
   - **📁 Subir Archivo**: Arrastra una imagen o haz clic para seleccionar
   - **📹 Tomar Foto**: Activa la cámara y captura una foto directamente (con contador de 3 segundos)
3. Haz clic en **"🔍 Analizar Imagen"**
4. **Nota**: El sistema usa automáticamente **ambos modelos** (PCA+SVM y TensorFlow) y muestra el mejor resultado
5. Verás el resultado:
   - **Predicción**: Humano o No Humano
   - **Confianza**: Porcentaje de certeza
   - **Probabilidades**: Para ambas categorías
   - **Tabla de Predicciones Recientes**: Se actualiza automáticamente
   - **Modal de imagen**: Haz clic en cualquier predicción para ver la imagen

### 4. Ver Historial

- **Predicciones**: **http://localhost:8000/history/**
  - Haz clic en cualquier fila para ver la imagen en un modal
- **Entrenamientos**: Se muestran en la página de entrenamiento con resultados detallados

---

## 🔧 Solución de Problemas

### Error: "No module named 'django'"

**Causa**: Las dependencias no están instaladas o el entorno virtual no está activado.

**Solución**:
1. Asegúrate de que el entorno virtual esté activado (deberías ver `(venv)` en tu terminal)
2. Instala las dependencias:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Error: "python: command not found" (Linux/Mac)

**Causa**: Python no está instalado o no está en el PATH.

**Solución**:
- **Linux**: `sudo apt-get install python3 python3-pip`
- **Mac**: `brew install python3` o descarga desde python.org
- Usa `python3` en lugar de `python` en los comandos

### Error: "No se reconoce como cmdlet" (PowerShell)

**Causa**: No estás en el directorio correcto o el script no existe.

**Solución**:
1. Verifica que estés en la carpeta `APE 4`:
   ```powershell
   pwd
   ```
2. Si no estás en la carpeta correcta:
   ```powershell
   cd "ruta\completa\al\proyecto\APE 4"
   ```

### Error: "No se puede cargar porque la ejecución de scripts está deshabilitada" (PowerShell)

**Causa**: La política de ejecución de PowerShell no permite scripts.

**Solución**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego intenta de nuevo activar el entorno virtual.

### Error: "No se encontraron imágenes válidas en el dataset"

**Causas posibles**:
1. Las carpetas `dataset/human/` o `dataset/non_human/` no existen
2. No hay imágenes en las carpetas
3. Las imágenes no tienen el formato correcto (deben ser JPG, PNG o JPEG)
4. Para imágenes humanas: no se detectan rostros en las imágenes

**Solución**:
1. Verifica que las carpetas existan y tengan imágenes:
   ```bash
   # Windows PowerShell
   Get-ChildItem dataset\human
   Get-ChildItem dataset\non_human
   
   # Linux/Mac
   ls dataset/human
   ls dataset/non_human
   ```
2. Para imágenes humanas, asegúrate de que los rostros sean claramente visibles y frontales
3. Usa la interfaz de captura para crear el dataset correctamente
4. Consulta `TIPS_FOTOS.md` para recomendaciones sobre cómo tomar fotos

### Error: "Se requiere al menos 2 clases para entrenar el modelo"

**Causa**: Solo tienes imágenes de una categoría (solo humanas o solo no humanas).

**Solución**: Agrega imágenes de la categoría faltante:
- Si solo tienes humanas → Captura/sube imágenes no humanas
- Si solo tienes no humanas → Captura/sube imágenes humanas

**Mínimo requerido**: Al menos 10-20 imágenes de cada categoría.

### Error: "Modelo no encontrado"

**Causa**: No has entrenado el modelo aún.

**Solución**: Entrena el modelo primero:
1. Ve a http://localhost:8000/train/
2. Haz clic en "Iniciar Entrenamiento"
3. Espera a que termine

### Error al acceder a la cámara

**Causas posibles**:
1. El navegador no tiene permisos para acceder a la cámara
2. Otra aplicación está usando la cámara
3. La cámara no está conectada
4. El navegador no soporta `getUserMedia` (navegadores muy antiguos)

**Solución**:
1. Asegúrate de permitir el acceso a la cámara cuando el navegador lo solicite
2. Cierra otras aplicaciones que puedan estar usando la cámara (Zoom, Teams, etc.)
3. Verifica que la cámara esté conectada y funcionando
4. Usa un navegador moderno (Chrome, Firefox, Edge actualizados)

### El servidor no inicia - Puerto ocupado

**Causa**: El puerto 8000 está ocupado por otra aplicación.

**Solución**: Usa otro puerto:
```bash
python manage.py runserver 8001
```

Luego accede a: **http://localhost:8001/**

### Error de encoding con emojis (Windows)

**Causa**: Problema de codificación en la consola de Windows.

**Solución**: Los emojis son solo visuales, el código funciona correctamente. Si quieres evitar el error:
```powershell
$env:PYTHONIOENCODING="utf-8"
python manage.py runserver
```

### Error: "cv2.imread can't open/read file" (OpenCV)

**Causa**: Ruta del archivo contiene caracteres especiales o espacios.

**Solución**: El sistema ya maneja esto automáticamente usando `cv2.imdecode`. Si persiste el error:
1. Evita usar caracteres especiales en nombres de archivos
2. Asegúrate de que las rutas no tengan espacios problemáticos
3. Usa la interfaz web para subir imágenes en lugar de colocarlas manualmente

### Dataset muy desbalanceado

**Problema**: Tienes muchas más imágenes de una categoría que de otra (ej: 440 humanas vs 24 no humanas).

**Solución**: 
1. Agrega más imágenes de la categoría con menos datos
2. Consulta `RECOMENDACIONES_DATASET.md` para recomendaciones detalladas
3. El sistema usa balanceo automático de clases, pero es mejor tener un dataset balanceado

### El entrenamiento tarda mucho tiempo

**Causa**: TensorFlow puede ser lento en CPUs, especialmente con datasets grandes.

**Solución**:
- Espera pacientemente (puede tardar 10-30 minutos)
- Considera usar una GPU si tienes una disponible
- Reduce el número de épocas en `recognition/training.py` si es necesario

---

## 🗂️ Estructura del Proyecto

```
APE 4/
├── face_recognition_system/      # Configuración principal de Django
│   ├── __init__.py
│   ├── settings.py               # Configuración del proyecto
│   ├── urls.py                   # URLs principales
│   ├── wsgi.py                   # WSGI para producción
│   └── asgi.py                   # ASGI para producción
│
├── recognition/                  # Aplicación principal
│   ├── __init__.py
│   ├── admin.py                 # Configuración del admin
│   ├── apps.py                  # Configuración de la app
│   ├── models.py                # Modelos de base de datos
│   ├── views.py                 # Vistas (lógica de negocio)
│   ├── urls.py                  # URLs de la app
│   ├── preprocessing.py         # Preprocesamiento de imágenes
│   ├── training.py              # Entrenamiento de modelos
│   ├── predictor.py             # Predicción con modelos
│   └── management/
│       └── commands/
│           └── train_model.py   # Comando para entrenar desde CLI
│
├── templates/                    # Plantillas HTML
│   ├── base.html                # Plantilla base
│   └── recognition/
│       ├── index.html           # Página principal
│       ├── capture.html         # Captura desde cámara
│       ├── dataset.html         # Gestión de dataset
│       ├── train.html           # Entrenamiento
│       ├── predict.html         # Predicción
│       └── history.html         # Historial
│
├── static/                       # Archivos estáticos
│   ├── css/
│   │   └── styles.css           # Estilos CSS
│   └── images/                  # Imágenes estáticas
│
├── dataset/                      # Dataset de imágenes
│   ├── human/                   # Imágenes humanas
│   └── non_human/               # Imágenes no humanas
│
├── models/                       # Modelos entrenados (se crean al entrenar)
│   ├── scaler.pkl              # Normalizador
│   ├── pca_model.pkl           # Modelo PCA
│   ├── svm_model.pkl           # Modelo SVM
│   └── tensorflow_model.h5     # Modelo TensorFlow
│
├── media/                        # Archivos subidos por usuarios
│   └── uploads/
│
├── venv/                         # Entorno virtual (NO incluir en Git)
├── manage.py                     # Script de gestión de Django
├── requirements.txt              # Dependencias del proyecto
├── db.sqlite3                    # Base de datos SQLite (se crea automáticamente)
├── iniciar_servidor.ps1          # Script para iniciar servidor (PowerShell)
├── iniciar_servidor.bat           # Script para iniciar servidor (CMD)
├── README.md                     # Este archivo
├── TIPS_FOTOS.md                 # Tips para tomar fotos
└── RECOMENDACIONES_DATASET.md    # Recomendaciones para el dataset
```

---

## 📚 Documentación Técnica

### Preprocesamiento de Imágenes

El sistema realiza los siguientes pasos de preprocesamiento:

1. **Detección de rostro** (solo para imágenes humanas):
   - Usa Haar Cascade de OpenCV con múltiples configuraciones
   - Aplica CLAHE (Contrast Limited Adaptive Histogram Equalization) para mejorar contraste
   - Intenta múltiples escalas y parámetros para robustez
   - Si no detecta rostro, procesa la imagen completa como fallback

2. **Conversión a escala de grises**:
   - Convierte imágenes RGB a escala de grises

3. **Aplicación de filtros**:
   - **Filtro bilateral**: Reduce ruido preservando bordes
   - **Ecualización de histograma**: Mejora el contraste

4. **Redimensionamiento**:
   - Redimensiona a 160x160 píxeles

5. **Normalización**:
   - Normaliza valores entre 0 y 1

### Modelos de IA

#### PCA + SVM

- **PCA (Principal Component Analysis)**:
  - Reduce la dimensionalidad de las características
  - Mantiene el 95% de la varianza por defecto
  - Acelera el entrenamiento y predicción

- **SVM (Support Vector Machine)**:
  - Kernel: RBF (Radial Basis Function)
  - Clasificador binario (Humano/No Humano)
  - Proporciona probabilidades de clase
  - Usa `class_weight='balanced'` para balancear clases desbalanceadas

#### TensorFlow/Keras

- **Arquitectura CNN**:
  - 3 capas convolucionales (32, 64, 64 filtros)
  - 2 capas de MaxPooling
  - 1 capa densa (64 neuronas)
  - Dropout (0.5) para regularización
  - Salida: 1 neurona con activación sigmoid

- **Entrenamiento**:
  - Optimizador: Adam
  - Loss: binary_crossentropy
  - Early stopping para evitar overfitting
  - Class weighting para balancear clases desbalanceadas

### Parámetros Configurables

Puedes modificar los parámetros en `recognition/training.py`:

```python
# PCA
pca_components = 0.95  # Proporción de varianza a mantener

# SVM
kernel = 'rbf'         # Tipo de kernel
C = 1.0                # Parámetro de regularización
gamma = 'scale'        # Parámetro del kernel

# TensorFlow
epochs = 50            # Número de épocas
batch_size = 32        # Tamaño del batch
```

---

## 📊 Resultados y Métricas

El sistema proporciona:

- **Predicción**: 0 (No Humano) o 1 (Humano)
- **Confianza**: Probabilidad de la predicción (0-100%)
- **Probabilidades**: Probabilidades para ambas clases
- **Accuracy**: Precisión del modelo en el conjunto de prueba
- **Reporte de clasificación**: Precision, Recall, F1-score

---

## 🎯 Flujo de Trabajo Recomendado

1. **Capturar Dataset** (40+ fotos de cada categoría)
   - Ve a `/capture/`
   - Captura 40+ fotos humanas
   - Captura 40+ fotos no humanas

2. **Entrenar Modelo**
   - Ve a `/train/`
   - Entrena ambos modelos (PCA+SVM y TensorFlow)
   - Revisa los resultados de accuracy

3. **Probar Modelo**
   - Ve a `/predict/`
   - Prueba con diferentes imágenes
   - Revisa la tabla de predicciones recientes

4. **Mejorar Dataset** (si es necesario)
   - Si la precisión es baja, agrega más imágenes
   - Asegúrate de tener variedad en las imágenes
   - Balancea el dataset (ratio 1:1 o máximo 2:1)
   - Reentrena el modelo

---

## 📝 Notas Importantes

- ⚠️ **Primera vez**: Debes entrenar el modelo antes de poder hacer predicciones
- ⚠️ **Dataset balanceado**: Se recomienda tener un número similar de imágenes en ambas categorías (ratio 1:1 o máximo 2:1)
- ⚠️ **Calidad de imágenes**: Las imágenes humanas deben tener rostros claramente visibles y frontales
- ⚠️ **Tiempo de entrenamiento**: Puede tardar varios minutos, especialmente TensorFlow (5-30 minutos)
- ⚠️ **Modelos guardados**: Los modelos se guardan en `models/` y se reutilizan hasta el próximo entrenamiento
- ⚠️ **Entorno virtual**: Siempre activa el entorno virtual antes de ejecutar comandos Python
- ⚠️ **Python 3.13**: Si tienes Python 3.13, las dependencias se instalarán automáticamente con versiones compatibles

---

## 🆘 Soporte

Si encuentras problemas:

1. Revisa la sección [Solución de Problemas](#-solución-de-problemas)
2. Verifica que todas las dependencias estén instaladas: `pip list`
3. Asegúrate de tener imágenes en ambas categorías
4. Verifica los logs en la consola para más detalles
5. Consulta los archivos de documentación adicional:
   - `TIPS_FOTOS.md` - Tips para tomar fotos
   - `RECOMENDACIONES_DATASET.md` - Recomendaciones para el dataset

---

## 📄 Licencia

Este proyecto fue desarrollado para fines académicos en la materia de Inteligencia Artificial.

---

## 👨‍💻 Autor

Desarrollado como proyecto académico para el reconocimiento de rostros humanos utilizando técnicas de Machine Learning y Deep Learning.

---

## 🎓 Actividades Implementadas

✅ Preprocesamiento de imágenes (escala de grises, filtros)  
✅ Generación de dataset etiquetado (0 = no humano, 1 = humano)  
✅ Entrenamiento de modelos de IA (PCA+SVM y TensorFlow)  
✅ Sistema de prueba en línea  
✅ Captura de imágenes desde cámara web  
✅ Interfaz web completa y profesional  

---

**¡Listo para usar! 🚀**
