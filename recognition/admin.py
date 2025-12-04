from django.contrib import admin
from .models import Prediction, TrainingHistory


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'prediction', 'confidence', 'image_path')
    list_filter = ('prediction', 'created_at')
    search_fields = ('image_path',)
    readonly_fields = ('created_at',)


@admin.register(TrainingHistory)
class TrainingHistoryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'accuracy', 'total_samples', 'human_samples', 'non_human_samples')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

