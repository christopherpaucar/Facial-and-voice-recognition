"""
URLs de la aplicación recognition
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('train/', views.train_view, name='train'),
    path('predict/', views.predict_view, name='predict'),
    path('history/', views.history_view, name='history'),
    path('dataset/', views.dataset_view, name='dataset'),
    path('capture/', views.capture_view, name='capture'),
    path('api/upload-dataset/', views.upload_dataset_image, name='upload_dataset'),
]

