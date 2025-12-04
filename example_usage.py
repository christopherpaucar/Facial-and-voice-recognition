"""
Script de ejemplo para usar el sistema de reconocimiento de rostros
Este script muestra cómo usar las clases principales del sistema
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_recognition_system.settings')
django.setup()

from recognition.preprocessing import ImagePreprocessor
from recognition.training import ModelTrainer
from recognition.predictor import FacePredictor
from django.conf import settings


def example_preprocessing():
    """Ejemplo de preprocesamiento de imágenes"""
    print("=" * 50)
    print("Ejemplo: Preprocesamiento de Imágenes")
    print("=" * 50)
    
    preprocessor = ImagePreprocessor()
    
    # Ejemplo con una imagen (reemplaza con la ruta de tu imagen)
    image_path = "dataset/human/ejemplo.jpg"
    
    if os.path.exists(image_path):
        processed = preprocessor.preprocess_for_training(image_path)
        if processed is not None:
            print(f"✅ Imagen preprocesada correctamente")
            print(f"   Dimensiones: {processed.shape}")
        else:
            print("❌ No se detectó rostro en la imagen")
    else:
        print(f"⚠️ Imagen no encontrada: {image_path}")


def example_training():
    """Ejemplo de entrenamiento"""
    print("\n" + "=" * 50)
    print("Ejemplo: Entrenamiento del Modelo")
    print("=" * 50)
    
    trainer = ModelTrainer(
        model_dir=settings.MODEL_DIR,
        dataset_dir=settings.DATASET_DIR
    )
    
    try:
        results = trainer.train_all(
            use_pca_svm=True,
            use_tensorflow=True,
            pca_components=0.95,
            epochs=50
        )
        
        print("\n✅ Entrenamiento completado!")
        print(f"   PCA+SVM Accuracy: {results.get('pca_svm', 'N/A')}")
        print(f"   TensorFlow Accuracy: {results.get('tensorflow', 'N/A')}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_prediction():
    """Ejemplo de predicción"""
    print("\n" + "=" * 50)
    print("Ejemplo: Predicción")
    print("=" * 50)
    
    # Intentar cargar el predictor
    try:
        predictor = FacePredictor(
            model_dir=settings.MODEL_DIR,
            use_model='pca_svm'
        )
        
        # Ejemplo con una imagen (reemplaza con la ruta de tu imagen)
        image_path = "dataset/human/ejemplo.jpg"
        
        if os.path.exists(image_path):
            result = predictor.predict_from_image(image_path)
            
            if result.get('prediction') is not None:
                print(f"✅ Predicción realizada")
                print(f"   Resultado: {result['label']}")
                print(f"   Confianza: {result['confidence']:.2%}")
                print(f"   Probabilidades:")
                print(f"     - Humano: {result['probabilities']['humano']:.2%}")
                print(f"     - No Humano: {result['probabilities']['no_humano']:.2%}")
            else:
                print(f"❌ {result.get('label', 'Error desconocido')}")
        else:
            print(f"⚠️ Imagen no encontrada: {image_path}")
            
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("   Por favor, entrena el modelo primero.")


if __name__ == "__main__":
    print("\n🤖 Sistema de Reconocimiento de Rostros - Ejemplos de Uso\n")
    
    # Ejecutar ejemplos
    example_preprocessing()
    # example_training()  # Descomenta para entrenar
    # example_prediction()  # Descomenta para predecir
    
    print("\n" + "=" * 50)
    print("Para más información, consulta el README.md")
    print("=" * 50)

