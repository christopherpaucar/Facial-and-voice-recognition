# 🚀 Inicio Rápido

## Pasos para comenzar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar base de datos
```bash
python manage.py migrate
```

### 3. Preparar el dataset

Crea las siguientes carpetas y coloca imágenes:
```
dataset/
├── human/          (imágenes con rostros humanos)
└── non_human/      (imágenes sin rostros humanos)
```

**Recomendación**: Al menos 50 imágenes de cada categoría.

### 4. Entrenar el modelo

**Opción A: Interfaz Web**
1. Inicia el servidor: `python manage.py runserver`
2. Ve a `http://localhost:8000/train/`
3. Haz clic en "Iniciar Entrenamiento"

**Opción B: Línea de comandos**
```bash
python manage.py train_model
```

### 5. Probar el modelo

1. Ve a `http://localhost:8000/predict/`
2. Sube una imagen
3. Selecciona el modelo (PCA+SVM o TensorFlow)
4. Haz clic en "Analizar Imagen"

## 📝 Notas Importantes

- **Primera vez**: Debes entrenar el modelo antes de poder hacer predicciones
- **Dataset**: Las imágenes humanas deben contener rostros visibles
- **Formatos**: JPG, PNG, JPEG son soportados
- **Tiempo de entrenamiento**: Puede tardar varios minutos dependiendo del tamaño del dataset

## 🆘 Solución de Problemas

### Error: "Modelo no encontrado"
- Asegúrate de haber entrenado el modelo primero
- Verifica que existan los archivos en `models/`:
  - `scaler.pkl`
  - `pca_model.pkl`
  - `svm_model.pkl`
  - `tensorflow_model.h5` (si entrenaste TensorFlow)

### Error: "No se detectó rostro"
- La imagen debe contener un rostro humano claramente visible
- Intenta con otra imagen o ajusta la iluminación

### Error: "No se encontraron imágenes en el dataset"
- Verifica que las carpetas `dataset/human/` y `dataset/non_human/` existan
- Asegúrate de que contengan imágenes en formato JPG, PNG o JPEG

## 📚 Más Información

Consulta el `README.md` para información detallada sobre el proyecto.

