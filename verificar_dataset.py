"""
Script para verificar el dataset y ver cuántas imágenes se pueden cargar
"""
import cv2
from pathlib import Path
from recognition.preprocessing import ImagePreprocessor

dataset_dir = Path('dataset')
preprocessor = ImagePreprocessor()

print("=" * 60)
print("VERIFICACIÓN DEL DATASET")
print("=" * 60)

# Verificar humanas
human_dir = dataset_dir / 'human'
if human_dir.exists():
    img_files = list(human_dir.glob('*.jpg')) + list(human_dir.glob('*.png')) + list(human_dir.glob('*.jpeg'))
    print(f"\n📁 Carpeta 'human': {len(img_files)} imágenes encontradas")
    
    loaded = 0
    failed = 0
    failed_files = []
    
    for img_file in img_files[:20]:  # Probar solo las primeras 20
        processed = preprocessor.preprocess_for_training(str(img_file))
        if processed is not None:
            loaded += 1
        else:
            failed += 1
            failed_files.append(img_file.name)
    
    print(f"   ✅ Procesadas correctamente: {loaded}")
    print(f"   ❌ Sin rostro detectado: {failed}")
    if failed_files:
        print(f"   Archivos sin rostro (primeros 5): {failed_files[:5]}")
else:
    print("\n⚠️ Carpeta 'human' no existe")

# Verificar non_human
non_human_dir = dataset_dir / 'non_human'
if non_human_dir.exists():
    img_files = list(non_human_dir.glob('*.jpg')) + list(non_human_dir.glob('*.png')) + list(non_human_dir.glob('*.jpeg'))
    print(f"\n📁 Carpeta 'non_human': {len(img_files)} imágenes encontradas")
else:
    print("\n⚠️ Carpeta 'non_human' no existe (se creará automáticamente)")

print("\n" + "=" * 60)
print("RECOMENDACIONES:")
print("=" * 60)
print("1. Para 'human': Asegúrate de que las imágenes tengan rostros claramente visibles")
print("2. Para 'non_human': Agrega imágenes de objetos, animales, paisajes, etc.")
print("3. Se recomienda al menos 20-30 imágenes de cada categoría para un buen entrenamiento")
print("=" * 60)

