from django.db import models
from django.conf import settings
from pathlib import Path


class TrainingHistory(models.Model):
    """Historial de entrenamientos del modelo"""
    created_at = models.DateTimeField(auto_now_add=True)
    accuracy = models.FloatField(null=True, blank=True)
    total_samples = models.IntegerField()
    human_samples = models.IntegerField()
    non_human_samples = models.IntegerField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Historial de Entrenamiento'
        verbose_name_plural = 'Historiales de Entrenamiento'

    def __str__(self):
        return f"Entrenamiento {self.created_at.strftime('%Y-%m-%d %H:%M')} - Accuracy: {self.accuracy:.2%}"


class Prediction(models.Model):
    """Registro de predicciones realizadas"""
    image_path = models.CharField(max_length=500)
    prediction = models.IntegerField()  # 0 = no humano, 1 = humano
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Predicción'
        verbose_name_plural = 'Predicciones'

    def get_prediction_display(self):
        """Retorna la etiqueta legible de la predicción"""
        return "Humano" if self.prediction == 1 else "No Humano"
    
    def get_image_url(self):
        """Convierte la ruta absoluta de la imagen a una URL relativa"""
        try:
            # Convertir ruta absoluta a relativa
            image_path = Path(self.image_path)
            media_root = Path(settings.MEDIA_ROOT)
            
            # Convertir a strings para comparación
            image_str = str(image_path.resolve())
            media_str = str(media_root.resolve())
            
            # Si la ruta está dentro de MEDIA_ROOT, convertir a URL
            if image_str.startswith(media_str):
                try:
                    relative_path = image_path.relative_to(media_root)
                    return f"{settings.MEDIA_URL}{relative_path.as_posix()}"
                except ValueError:
                    # Si no se puede hacer relative_to, extraer manualmente
                    if media_str in image_str:
                        relative = image_str.replace(media_str, '').lstrip('\\/').replace('\\', '/')
                        return f"{settings.MEDIA_URL}{relative}"
            
            # Si la ruta contiene 'uploads' o 'media', extraer el nombre del archivo
            if 'uploads' in str(image_path) or 'media' in str(image_path):
                filename = image_path.name
                return f"{settings.MEDIA_URL}uploads/{filename}"
            
            # Fallback: usar la ruta tal cual si empieza con /media/
            image_path_str = str(image_path)
            if image_path_str.startswith('/media/') or image_path_str.startswith('media/'):
                return image_path_str if image_path_str.startswith('/') else f"/{image_path_str}"
            
            # Último recurso: solo el nombre del archivo en uploads
            return f"{settings.MEDIA_URL}uploads/{image_path.name}"
        except Exception:
            # Si hay algún error, retornar una ruta por defecto
            try:
                return f"{settings.MEDIA_URL}uploads/{Path(self.image_path).name}"
            except:
                return f"{settings.MEDIA_URL}uploads/default.jpg"
    
    def __str__(self):
        label = self.get_prediction_display()
        return f"{label} ({self.confidence:.2%}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

