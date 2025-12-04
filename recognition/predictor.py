"""
Módulo de predicción usando los modelos entrenados
"""
import os
import numpy as np
import joblib
import cv2
from pathlib import Path
from .preprocessing import ImagePreprocessor
import tensorflow as tf


class FacePredictor:
    """Clase para realizar predicciones con los modelos entrenados"""
    
    def __init__(self, model_dir='models', use_model='pca_svm'):
        """
        Args:
            model_dir: Directorio donde están los modelos
            use_model: Modelo a usar ('pca_svm' o 'tensorflow')
        """
        self.model_dir = Path(model_dir)
        self.use_model = use_model
        self.preprocessor = ImagePreprocessor()
        
        # Cargar modelos
        self._load_models()
    
    def _load_models(self):
        """Carga los modelos desde disco"""
        if self.use_model == 'pca_svm':
            try:
                self.scaler = joblib.load(self.model_dir / 'scaler.pkl')
                self.pca = joblib.load(self.model_dir / 'pca_model.pkl')
                self.svm = joblib.load(self.model_dir / 'svm_model.pkl')
                print("✅ Modelos PCA + SVM cargados correctamente")
            except FileNotFoundError as e:
                raise FileNotFoundError(
                    f"Modelos PCA + SVM no encontrados en {self.model_dir}. "
                    "Por favor, entrena el modelo primero."
                ) from e
        
        elif self.use_model == 'tensorflow':
            try:
                self.tf_model = tf.keras.models.load_model(self.model_dir / 'tensorflow_model.h5')
                print("✅ Modelo TensorFlow cargado correctamente")
            except FileNotFoundError as e:
                raise FileNotFoundError(
                    f"Modelo TensorFlow no encontrado en {self.model_dir}. "
                    "Por favor, entrena el modelo primero."
                ) from e
        else:
            raise ValueError(f"Modelo desconocido: {self.use_model}. Use 'pca_svm' o 'tensorflow'")
    
    def predict_from_image(self, image_path):
        """
        Realiza una predicción desde una imagen
        
        Args:
            image_path: Ruta a la imagen
            
        Returns:
            dict: {
                'prediction': 0 o 1 (0 = no humano, 1 = humano),
                'confidence': probabilidad de confianza,
                'label': 'Humano' o 'No Humano'
            }
        """
        import cv2
        import numpy as np
        
        # Procesar imagen: intentar detectar rostro, pero si no se detecta, procesar imagen completa
        # El modelo decidirá si es humano o no basándose en las características de la imagen
        processed = self.preprocessor.preprocess_for_training(
            image_path,
            apply_filters=True,
            detect_face=True,  # Intentar detectar rostro primero
            remove_bg=False
        )
        
        if processed is None:
            return {
                'prediction': None,
                'confidence': 0.0,
                'label': 'Error: No se pudo procesar la imagen',
                'error': 'Error al procesar imagen'
            }
        
        # Realizar predicción según el modelo
        if self.use_model == 'pca_svm':
            return self._predict_pca_svm(processed)
        else:
            return self._predict_tensorflow(processed)
    
    def predict_from_array(self, image_array):
        """
        Realiza una predicción desde un array numpy
        
        Args:
            image_array: Array numpy de la imagen (BGR)
            
        Returns:
            dict: Resultado de la predicción
        """
        # Preprocesar: intentar detectar rostro, pero si falla procesar imagen completa
        processed = self.preprocessor.preprocess_pipeline(
            image_array,
            apply_filters=True,
            detect_face=True,  # Intentar detectar rostro primero
            allow_no_face=True  # Si no detecta rostro, procesar imagen completa
        )
        
        if processed is None:
            return {
                'prediction': None,
                'confidence': 0.0,
                'label': 'Error: No se pudo procesar la imagen',
                'error': 'Error al procesar imagen'
            }
        
        # Aplanar
        processed_flat = processed.flatten()
        
        # Realizar predicción
        if self.use_model == 'pca_svm':
            return self._predict_pca_svm(processed_flat)
        else:
            return self._predict_tensorflow(processed_flat)
    
    def _predict_pca_svm(self, features):
        """
        Predicción usando PCA + SVM
        
        Args:
            features: Array de características aplanado
            
        Returns:
            dict: Resultado de la predicción
        """
        # Normalizar
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # PCA
        features_pca = self.pca.transform(features_scaled)
        
        # Predicción
        probabilities = self.svm.predict_proba(features_pca)[0]
        
        # Determinar predicción basada en la probabilidad más alta
        # probabilities[0] = No Humano, probabilities[1] = Humano
        if probabilities[1] > probabilities[0]:
            prediction = 1  # Humano
            confidence = float(probabilities[1])
        else:
            prediction = 0  # No Humano
            confidence = float(probabilities[0])
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'label': 'Humano' if prediction == 1 else 'No Humano',
            'probabilities': {
                'no_humano': float(probabilities[0]),
                'humano': float(probabilities[1])
            }
        }
    
    def _predict_tensorflow(self, features):
        """
        Predicción usando TensorFlow
        
        Args:
            features: Array de características aplanado
            
        Returns:
            dict: Resultado de la predicción
        """
        # Redimensionar para CNN
        img_size = int(np.sqrt(len(features)))
        features_reshaped = features.reshape(1, img_size, img_size, 1).astype('float32')
        
        # Predicción
        probabilities = self.tf_model.predict(features_reshaped, verbose=0)[0]
        
        # probabilities[0] es la probabilidad de "Humano" en TensorFlow
        prob_humano = float(probabilities[0])
        prob_no_humano = float(1 - probabilities[0])
        
        # Determinar predicción basada en la probabilidad más alta
        if prob_humano > prob_no_humano:
            prediction = 1  # Humano
            confidence = prob_humano
        else:
            prediction = 0  # No Humano
            confidence = prob_no_humano
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'label': 'Humano' if prediction == 1 else 'No Humano',
            'probabilities': {
                'no_humano': prob_no_humano,
                'humano': prob_humano
            }
        }

