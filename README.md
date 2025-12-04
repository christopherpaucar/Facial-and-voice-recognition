# 🤖 Sistema de Reconocimiento de Rostros Humanos

Sistema on-line de visión por computadora para el reconocimiento de rostros humanos utilizando inteligencia artificial. Desarrollado con Django, PCA, SVM y TensorFlow.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Configuración Inicial](#-configuración-inicial)
- [Uso del Sistema](#-uso-del-sistema)
- [Estructura del Proyecto](#️-estructura-del-proyecto)
- [Solución de Problemas](#-solución-de-problemas)
- [Documentación Técnica](#-documentación-técnica)

---

## 🎯 Características

- ✅ **Preprocesamiento avanzado**: Conversión a escala de grises, filtros Gaussianos, ecualización de histograma, filtros bilaterales
- ✅ **Detección automática**: Detección de rostros usando Haar Cascade de OpenCV
- ✅ **Múltiples modelos de IA**:
  - **PCA + SVM**: Reducción de dimensionalidad con PCA y clasificación con Support Vector Machine
  - **TensorFlow/Keras**: Red neuronal convolucional (CNN) para clasificación
- ✅ **Interfaz web completa**: Interfaz Django moderna y responsive
- ✅ **Captura desde cámara**: Sistema integrado para capturar fotos directamente desde la cámara web
- ✅ **Gestión de dataset**: Sistema para subir y organizar imágenes de entrenamiento
- ✅ **Historial completo**: Registro de predicciones y entrenamientos realizados

---

## 💻 Requisitos del Sistema

### Software Requerido

- **Python**: 3.8 o superior (recomendado: 3.10+)
- **Sistema Operativo**: Windows, Linux o macOS
- **Navegador Web**: Chrome, Firefox, Edge (últimas versiones)
- **Cámara Web**: Opcional, para captura de imágenes

### Hardware Recomendado

- **RAM**: Mínimo 4GB (recomendado: 8GB+)
- **Procesador**: Mínimo 2 núcleos (recomendado: 4+ núcleos)
- **Espacio en disco**: Mínimo 2GB libres
- **GPU**: Opcional, pero recomendada para entrenamiento con TensorFlow

---

## 🚀 Instalación

### Paso 1: Clonar o Descargar el Proyecto

Si tienes el proyecto en un repositorio:
```bash
git clone https://github.com/christopherpaucar/Facial-and-voice-recognition.git
cd "APE 4"
```

O simplemente navega a la carpeta del proyecto:
```bash
cd "APE 4"
```

### Paso 2: Crear Entorno Virtual (Recomendado)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> **Nota**: Si tienes problemas con la ejecución de scripts en PowerShell, ejecuta:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Paso 3: Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Tiempo estimado**: 5-15 minutos (dependiendo de tu conexión)

> **⚠️ Importante**: Si tienes Python 3.13, las dependencias se instalarán automáticamente con versiones compatibles.

### Paso 4: Verificar Instalación

```bash
python manage.py check
```

Si todo está correcto, verás:
```
System check identified no issues (0 silenced).
```

---

## ⚙️ Configuración Inicial

### Paso 1: Configurar Base de Datos

```bash
python manage.py migrate
```

Esto creará las tablas necesarias en la base de datos SQLite.

### Paso 2: Crear Superusuario (Opcional)

Para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear un usuario administrador.

### Paso 3: Crear Carpetas del Dataset

Las carpetas se crean automáticamente, pero puedes verificarlas:

```bash
# Windows PowerShell
New-Item -ItemType Directory -Path "dataset\human" -Force
New-Item -ItemType Directory -Path "dataset\non_human" -Force

# Linux/Mac
mkdir -p dataset/human dataset/non_human
```

### Paso 4: Iniciar el Servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: **http://localhost:8000**

> **Nota**: Si el puerto 8000 está ocupado, puedes usar otro puerto:
> ```bash
> python manage.py runserver 8001
> ```

---

## 🎓 Uso del Sistema

### 1. Preparar el Dataset

El sistema requiere imágenes en **DOS categorías**:

#### Opción A: Captura desde Cámara (Recomendado)

1. Abre tu navegador y ve a: **http://localhost:8000/capture/**
2. Selecciona la categoría:
   - **"Humano"**: Para capturar rostros humanos
   - **"No Humano"**: Para capturar objetos, animales, paisajes, etc.
3. Haz clic en **"Iniciar Cámara y Capturar 40 Fotos"**
4. Permite el acceso a tu cámara cuando el navegador lo solicite
5. Las 40 fotos se capturarán automáticamente

#### Opción B: Subir Imágenes Manualmente

1. Ve a: **http://localhost:8000/dataset/**
2. Usa los formularios para subir imágenes:
   - Sube imágenes humanas en "Subir Imagen Humana"
   - Sube imágenes no humanas en "Subir Imagen No Humana"

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
- **Formatos soportados**: JPG, PNG, JPEG
- **Para humanas**: Asegúrate de que los rostros sean claramente visibles

### 2. Entrenar el Modelo

#### Opción A: Interfaz Web (Recomendado)

1. Ve a: **http://localhost:8000/train/**
2. Selecciona qué modelos entrenar:
   - ☑️ **Entrenar modelo PCA + SVM** (más rápido)
   - ☑️ **Entrenar modelo TensorFlow** (más preciso)
3. Haz clic en **"🚀 Iniciar Entrenamiento"**
4. Espera a que termine el proceso (puede tardar varios minutos)

#### Opción B: Línea de Comandos

```bash
python manage.py train_model
```

O con opciones personalizadas:

```bash
# Solo PCA+SVM
python manage.py train_model --pca-svm-only

# Solo TensorFlow
python manage.py train_model --tensorflow-only

# Con parámetros personalizados
python manage.py train_model --pca-components 0.90 --epochs 100
```

**Tiempo estimado de entrenamiento**:
- PCA+SVM: 1-5 minutos (dependiendo del dataset)
- TensorFlow: 5-30 minutos (dependiendo del dataset y hardware)

### 3. Probar el Modelo

1. Ve a: **http://localhost:8000/predict/**
2. Haz clic en **"Seleccionar Imagen"** y elige una imagen
3. Selecciona el modelo a usar:
   - **PCA + SVM**: Más rápido, buena precisión
   - **TensorFlow**: Más lento, mayor precisión
4. Haz clic en **"🔍 Analizar Imagen"**
5. Verás el resultado:
   - **Predicción**: Humano o No Humano
   - **Confianza**: Porcentaje de certeza
   - **Probabilidades**: Para ambas categorías

### 4. Ver Historial

- **Predicciones**: **http://localhost:8000/history/**
- **Entrenamientos**: Se muestran en la página de entrenamiento

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
│   └── css/
│       └── styles.css           # Estilos CSS
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
├── manage.py                     # Script de gestión de Django
├── requirements.txt              # Dependencias del proyecto
├── db.sqlite3                    # Base de datos SQLite (se crea automáticamente)
└── README.md                     # Este archivo
```

---

## 🔧 Solución de Problemas

### Error: "No module named 'django'"

**Solución**: Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "No se encontraron imágenes en el dataset"

**Causas posibles**:
1. Las carpetas `dataset/human/` o `dataset/non_human/` no existen
2. No hay imágenes en las carpetas
3. Las imágenes no tienen el formato correcto (deben ser JPG, PNG o JPEG)
4. Para imágenes humanas: no se detectan rostros en las imágenes

**Solución**:
1. Verifica que las carpetas existan y tengan imágenes
2. Para imágenes humanas, asegúrate de que los rostros sean claramente visibles
3. Usa la interfaz de captura para crear el dataset correctamente

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

**Solución**:
1. Asegúrate de permitir el acceso a la cámara cuando el navegador lo solicite
2. Cierra otras aplicaciones que puedan estar usando la cámara
3. Verifica que la cámara esté conectada y funcionando

### El servidor no inicia

**Causa**: El puerto 8000 está ocupado.

**Solución**: Usa otro puerto:
```bash
python manage.py runserver 8001
```

### Error de encoding con emojis (Windows)

**Causa**: Problema de codificación en la consola de Windows.

**Solución**: Los emojis son solo visuales, el código funciona correctamente. Si quieres evitar el error, puedes ejecutar:
```powershell
$env:PYTHONIOENCODING="utf-8"
python manage.py runserver
```

---

## 📚 Documentación Técnica

### Preprocesamiento de Imágenes

El sistema realiza los siguientes pasos de preprocesamiento:

1. **Detección de rostro** (solo para imágenes humanas):
   - Usa Haar Cascade de OpenCV
   - Recorta el rostro detectado

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

1. **Capturar Dataset** (40 fotos de cada categoría)
   - Ve a `/capture/`
   - Captura 40 fotos humanas
   - Captura 40 fotos no humanas

2. **Entrenar Modelo**
   - Ve a `/train/`
   - Entrena ambos modelos (PCA+SVM y TensorFlow)

3. **Probar Modelo**
   - Ve a `/predict/`
   - Prueba con diferentes imágenes
   - Compara resultados entre modelos

4. **Mejorar Dataset** (si es necesario)
   - Si la precisión es baja, agrega más imágenes
   - Asegúrate de tener variedad en las imágenes
   - Reentrena el modelo

---

## 📝 Notas Importantes

- ⚠️ **Primera vez**: Debes entrenar el modelo antes de poder hacer predicciones
- ⚠️ **Dataset balanceado**: Se recomienda tener un número similar de imágenes en ambas categorías
- ⚠️ **Calidad de imágenes**: Las imágenes humanas deben tener rostros claramente visibles
- ⚠️ **Tiempo de entrenamiento**: Puede tardar varios minutos, especialmente TensorFlow
- ⚠️ **Modelos guardados**: Los modelos se guardan en `models/` y se reutilizan hasta el próximo entrenamiento

---

## 🆘 Soporte

Si encuentras problemas:

1. Revisa la sección [Solución de Problemas](#-solución-de-problemas)
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de tener imágenes en ambas categorías
4. Verifica los logs en la consola para más detalles

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

Para comenzar, ejecuta:
```bash
python manage.py runserver
```

Y visita: **http://localhost:8000**
