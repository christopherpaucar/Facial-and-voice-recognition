# 📊 Recomendaciones para Mejorar el Dataset

## ⚠️ Problema Actual

Tu dataset está **muy desbalanceado**:
- **440 imágenes humanas** 
- **24 imágenes no humanas**
- **Ratio: 18.3:1** (muy desbalanceado)

Esto causa que el modelo esté **sesgado hacia "Humano"** y clasifique incorrectamente objetos como humanos.

## ✅ Soluciones Implementadas

He agregado **balanceo de clases** en el entrenamiento:
- ✅ SVM ahora usa `class_weight='balanced'`
- ✅ TensorFlow ahora usa `class_weight` para balancear

Esto ayudará, pero **NO es suficiente**. Necesitas más datos.

## 🎯 Recomendaciones

### Opción 1: Agregar Más Imágenes No Humanas (RECOMENDADO)

**Mínimo necesario:**
- Al menos **100-200 imágenes no humanas** (idealmente 300-400)
- Ratio ideal: **1:1 o máximo 2:1**

**Tipos de imágenes no humanas que puedes agregar:**
- 📱 Teléfonos, tablets, computadoras
- 🚗 Carros, motos, bicicletas
- 🏠 Casas, edificios, paisajes
- 🐕 Animales (perros, gatos, etc.)
- 🍎 Frutas, objetos cotidianos
- 📚 Libros, cuadernos, objetos de escritorio
- 🎮 Controles de videojuegos, consolas
- 🪑 Muebles, sillas, mesas

### Opción 2: Reducir Imágenes Humanas

Si no puedes agregar más imágenes no humanas:
- Reduce las imágenes humanas a **100-150** (manteniendo las mejores)
- Mantén **100-150 imágenes no humanas**
- Ratio: **1:1** (balanceado)

### Opción 3: Usar Data Augmentation

Puedes duplicar las imágenes no humanas con transformaciones:
- Rotaciones
- Cambios de brillo/contraste
- Espejos horizontales
- Recortes aleatorios

## 📝 Cómo Agregar Imágenes

1. **Desde la interfaz web:**
   - Ve a: http://localhost:8000/capture/
   - Selecciona "No Humano"
   - Captura o sube imágenes

2. **Directamente en la carpeta:**
   - Coloca imágenes en: `dataset/non_human/`
   - Formatos: JPG, PNG, JPEG

## 🔄 Después de Agregar Imágenes

1. **Reentrena el modelo:**
   - Ve a: http://localhost:8000/train/
   - Haz clic en "Iniciar Entrenamiento"
   - Espera a que termine

2. **Prueba el modelo:**
   - Ve a: http://localhost:8000/predict/
   - Prueba con diferentes imágenes

## 📈 Resultados Esperados

Con un dataset balanceado:
- ✅ Mejor precisión en ambas clases
- ✅ Menos falsos positivos (objetos clasificados como humanos)
- ✅ Menos falsos negativos (humanos clasificados como objetos)
- ✅ Confianza más precisa en las predicciones

---

**Nota:** El balanceo de clases ayuda, pero **nada reemplaza tener un dataset balanceado**. Agrega más imágenes no humanas para mejores resultados.

