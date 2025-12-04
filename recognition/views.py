"""
Vistas del sistema de reconocimiento de rostros
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import json
from pathlib import Path

import numpy as np
from .predictor import FacePredictor
from .training import ModelTrainer
from .models import Prediction, TrainingHistory


def index(request):
    """Página principal"""
    return render(request, 'recognition/index.html')


def train_view(request):
    """Vista para entrenar el modelo"""
    if request.method == 'POST':
        try:
            use_pca_svm = request.POST.get('use_pca_svm', 'on') == 'on'
            use_tensorflow = request.POST.get('use_tensorflow', 'on') == 'on'
            
            trainer = ModelTrainer(
                model_dir=settings.MODEL_DIR,
                dataset_dir=settings.DATASET_DIR
            )
            
            # Cargar dataset primero para obtener estadísticas
            X, y = trainer.load_dataset()
            total_samples = len(X)
            human_samples = int(np.sum(y == 1))
            non_human_samples = int(np.sum(y == 0))
            
            results = trainer.train_all(
                use_pca_svm=use_pca_svm,
                use_tensorflow=use_tensorflow,
                pca_components=0.95,
                epochs=50,
                batch_size=32
            )
            
            # Guardar en historial
            accuracy = results.get('pca_svm') or results.get('tensorflow') or 0.0
            TrainingHistory.objects.create(
                accuracy=accuracy,
                total_samples=total_samples,
                human_samples=human_samples,
                non_human_samples=non_human_samples,
                notes=f"PCA+SVM: {use_pca_svm}, TensorFlow: {use_tensorflow}"
            )
            
            return JsonResponse({
                'success': True,
                'results': results,
                'message': 'Modelo entrenado exitosamente'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    # GET: Mostrar página de entrenamiento
    recent_trainings = TrainingHistory.objects.all()[:10]
    return render(request, 'recognition/train.html', {
        'recent_trainings': recent_trainings
    })


@csrf_exempt
def predict_view(request):
    """Vista para realizar predicciones"""
    if request.method == 'POST':
        try:
            # Obtener imagen
            if 'image' not in request.FILES:
                return JsonResponse({
                    'success': False,
                    'error': 'No se proporcionó ninguna imagen'
                }, status=400)
            
            image_file = request.FILES['image']
            model_type = request.POST.get('model_type', 'pca_svm')
            
            # Guardar imagen temporalmente
            upload_dir = settings.MEDIA_ROOT / 'uploads'
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = upload_dir / image_file.name
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # Realizar predicción
            predictor = FacePredictor(
                model_dir=settings.MODEL_DIR,
                use_model=model_type
            )
            
            result = predictor.predict_from_image(str(file_path))
            
            # Guardar predicción en BD
            if result.get('prediction') is not None:
                Prediction.objects.create(
                    image_path=str(file_path),
                    prediction=result['prediction'],
                    confidence=result['confidence']
                )
            
            # Limpiar archivo temporal después de un tiempo (opcional)
            # os.remove(file_path)
            
            return JsonResponse({
                'success': True,
                'result': result
            })
            
        except FileNotFoundError as e:
            return JsonResponse({
                'success': False,
                'error': 'Modelo no encontrado. Por favor, entrena el modelo primero.'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    # GET: Mostrar página de predicción
    recent_predictions = Prediction.objects.all()[:10]
    return render(request, 'recognition/predict.html', {
        'recent_predictions': recent_predictions
    })


def history_view(request):
    """Vista para ver el historial de predicciones y entrenamientos"""
    predictions = Prediction.objects.all()[:50]
    trainings = TrainingHistory.objects.all()[:20]
    
    return render(request, 'recognition/history.html', {
        'predictions': predictions,
        'trainings': trainings
    })


def dataset_view(request):
    """Vista para gestionar el dataset"""
    human_dir = settings.DATASET_DIR / 'human'
    non_human_dir = settings.DATASET_DIR / 'non_human'
    
    human_count = len(list(human_dir.glob('*.jpg')) + list(human_dir.glob('*.png')) + list(human_dir.glob('*.jpeg'))) if human_dir.exists() else 0
    non_human_count = len(list(non_human_dir.glob('*.jpg')) + list(non_human_dir.glob('*.png')) + list(non_human_dir.glob('*.jpeg'))) if non_human_dir.exists() else 0
    
    return render(request, 'recognition/dataset.html', {
        'human_count': human_count,
        'non_human_count': non_human_count,
        'total_count': human_count + non_human_count
    })


@csrf_exempt
def upload_dataset_image(request):
    """Vista para subir imágenes al dataset"""
    if request.method == 'POST':
        try:
            if 'image' not in request.FILES:
                return JsonResponse({
                    'success': False,
                    'error': 'No se proporcionó ninguna imagen'
                }, status=400)
            
            image_file = request.FILES['image']
            label = request.POST.get('label', 'human')  # 'human' o 'non_human'
            
            # Crear directorio si no existe
            target_dir = settings.DATASET_DIR / label
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Generar nombre único si no viene nombre o si es captura de cámara
            if not image_file.name or image_file.name.startswith('capture_'):
                import datetime
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                filename = f'capture_{timestamp}.jpg'
            else:
                filename = image_file.name
            
            # Guardar imagen
            file_path = target_dir / filename
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            return JsonResponse({
                'success': True,
                'message': f'Imagen guardada en {label}',
                'path': str(file_path)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def capture_view(request):
    """Vista para capturar fotos desde la cámara"""
    return render(request, 'recognition/capture.html')

