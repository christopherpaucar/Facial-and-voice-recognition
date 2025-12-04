"""
Módulo de preprocesamiento de imágenes
Incluye conversión a escala de grises y aplicación de filtros
"""
import cv2
import numpy as np


class ImagePreprocessor:
    """Clase para preprocesar imágenes de rostros"""
    
    def __init__(self, target_size=(160, 160)):
        """
        Args:
            target_size: Tamaño objetivo para redimensionar las imágenes
        """
        self.target_size = target_size
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def detect_face(self, image):
        """
        Detecta un rostro en la imagen usando Haar Cascade
        
        Args:
            image: Imagen en formato BGR (OpenCV)
            
        Returns:
            Tupla (x, y, w, h) con las coordenadas del rostro, o None si no se detecta
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        if len(faces) > 0:
            # Retornar el rostro más grande
            faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
            return faces[0]
        return None
    
    def to_grayscale(self, image):
        """
        Convierte una imagen a escala de grises
        
        Args:
            image: Imagen en formato BGR
            
        Returns:
            Imagen en escala de grises
        """
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    
    def apply_gaussian_filter(self, image, kernel_size=5):
        """
        Aplica un filtro Gaussiano para suavizar la imagen
        
        Args:
            image: Imagen en escala de grises
            kernel_size: Tamaño del kernel (debe ser impar)
            
        Returns:
            Imagen filtrada
        """
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    def apply_histogram_equalization(self, image):
        """
        Aplica ecualización de histograma para mejorar el contraste
        
        Args:
            image: Imagen en escala de grises
            
        Returns:
            Imagen con histograma ecualizado
        """
        return cv2.equalizeHist(image)
    
    def apply_bilateral_filter(self, image, d=9, sigma_color=75, sigma_space=75):
        """
        Aplica un filtro bilateral para reducir ruido preservando bordes
        
        Args:
            image: Imagen en escala de grises
            d: Diámetro de la vecindad
            sigma_color: Filtro sigma en el espacio de color
            sigma_space: Filtro sigma en el espacio de coordenadas
            
        Returns:
            Imagen filtrada
        """
        return cv2.bilateralFilter(image, d, sigma_color, sigma_space)
    
    def normalize(self, image):
        """
        Normaliza la imagen a valores entre 0 y 1
        
        Args:
            image: Imagen en escala de grises
            
        Returns:
            Imagen normalizada
        """
        return image.astype(np.float32) / 255.0
    
    def resize(self, image, size=None):
        """
        Redimensiona la imagen al tamaño objetivo
        
        Args:
            image: Imagen a redimensionar
            size: Tamaño objetivo (ancho, alto). Si es None, usa self.target_size
            
        Returns:
            Imagen redimensionada
        """
        if size is None:
            size = self.target_size
        return cv2.resize(image, size)
    
    def preprocess_pipeline(self, image, apply_filters=True, detect_face=True):
        """
        Pipeline completo de preprocesamiento
        
        Args:
            image: Imagen original en formato BGR
            apply_filters: Si True, aplica filtros de suavizado
            detect_face: Si True, detecta y recorta el rostro
            
        Returns:
            Imagen preprocesada lista para el modelo, o None si no se detecta rostro
        """
        # 1. Detectar rostro si es necesario
        if detect_face:
            face_coords = self.detect_face(image)
            if face_coords is None:
                return None
            x, y, w, h = face_coords
            # Recortar el rostro con un margen
            margin = 20
            x = max(0, x - margin)
            y = max(0, y - margin)
            w = min(image.shape[1] - x, w + 2 * margin)
            h = min(image.shape[0] - y, h + 2 * margin)
            image = image[y:y+h, x:x+w]
        
        # 2. Convertir a escala de grises
        gray = self.to_grayscale(image)
        
        # 3. Aplicar filtros si se solicita
        if apply_filters:
            # Aplicar filtro bilateral para reducir ruido
            gray = self.apply_bilateral_filter(gray)
            # Aplicar ecualización de histograma
            gray = self.apply_histogram_equalization(gray)
        
        # 4. Redimensionar
        resized = self.resize(gray)
        
        # 5. Normalizar
        normalized = self.normalize(resized)
        
        return normalized
    
    def preprocess_for_training(self, image_path, apply_filters=True):
        """
        Preprocesa una imagen desde archivo para entrenamiento
        
        Args:
            image_path: Ruta a la imagen
            apply_filters: Si True, aplica filtros
            
        Returns:
            Array numpy con la imagen preprocesada, o None si falla
        """
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        processed = self.preprocess_pipeline(image, apply_filters=apply_filters, detect_face=True)
        if processed is None:
            return None
        
        # Aplanar para el modelo
        return processed.flatten()

