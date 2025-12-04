from django.db import models


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
    
    def __str__(self):
        label = self.get_prediction_display()
        return f"{label} ({self.confidence:.2%}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

