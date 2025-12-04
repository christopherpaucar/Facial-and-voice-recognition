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
        # Cargar el cascade classifier con manejo de errores
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Verificar que se cargó correctamente
        if self.face_cascade.empty():
            # Intentar con ruta alternativa
            import os
            alt_path = os.path.join(os.path.dirname(cv2.__file__), 'data', 'haarcascade_frontalface_default.xml')
            self.face_cascade = cv2.CascadeClassifier(alt_path)
            
            if self.face_cascade.empty():
                print("⚠️ Advertencia: No se pudo cargar el cascade classifier. La detección de rostros puede fallar.")
    
    def detect_face(self, image):
        """
        Detecta un rostro en la imagen usando Haar Cascade con múltiples intentos
        
        Args:
            image: Imagen en formato BGR (OpenCV)
            
        Returns:
            Tupla (x, y, w, h) con las coordenadas del rostro, o None si no se detecta
        """
        try:
            # Verificar que el cascade esté cargado
            if self.face_cascade.empty():
                return None
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Mejorar contraste para mejor detección
            try:
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                gray_enhanced = clahe.apply(gray)
            except:
                gray_enhanced = gray
            
            # Intentar con diferentes configuraciones de parámetros
            configs = [
                {'scaleFactor': 1.1, 'minNeighbors': 3, 'minSize': (30, 30)},
                {'scaleFactor': 1.05, 'minNeighbors': 2, 'minSize': (20, 20)},
                {'scaleFactor': 1.03, 'minNeighbors': 1, 'minSize': (15, 15)},
                {'scaleFactor': 1.1, 'minNeighbors': 2, 'minSize': (25, 25)},
            ]
            
            for config in configs:
                try:
                    faces = self.face_cascade.detectMultiScale(
                        gray_enhanced,
                        scaleFactor=config['scaleFactor'],
                        minNeighbors=config['minNeighbors'],
                        minSize=config['minSize'],
                        flags=cv2.CASCADE_SCALE_IMAGE
                    )
                    
                    if len(faces) > 0:
                        # Retornar el rostro más grande
                        faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
                        return faces[0]
                except:
                    continue
            
            # Si aún no se detecta, intentar con la imagen original sin mejora
            for config in configs[:2]:  # Solo los primeros 2 configs
                try:
                    faces = self.face_cascade.detectMultiScale(
                        gray,
                        scaleFactor=config['scaleFactor'],
                        minNeighbors=config['minNeighbors'],
                        minSize=config['minSize']
                    )
                    
                    if len(faces) > 0:
                        faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
                        return faces[0]
                except:
                    continue
            
            return None
        except Exception as e:
            # Si hay cualquier error, retornar None para que use el fallback
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
    
    def preprocess_pipeline(self, image, apply_filters=True, detect_face=True, allow_no_face=False):
        """
        Pipeline completo de preprocesamiento
        
        Args:
            image: Imagen original en formato BGR
            apply_filters: Si True, aplica filtros de suavizado
            detect_face: Si True, detecta y recorta el rostro
            allow_no_face: Si True, procesa la imagen completa si no se detecta rostro
            
        Returns:
            Imagen preprocesada lista para el modelo, o None si no se detecta rostro y allow_no_face=False
        """
        # 1. Detectar rostro si es necesario
        if detect_face:
            try:
                face_coords = self.detect_face(image)
                if face_coords is not None:
                    x, y, w, h = face_coords
                    # Recortar el rostro con un margen
                    margin = 20
                    x = max(0, x - margin)
                    y = max(0, y - margin)
                    w = min(image.shape[1] - x, w + 2 * margin)
                    h = min(image.shape[0] - y, h + 2 * margin)
                    image = image[y:y+h, x:x+w]
                elif not allow_no_face:
                    return None
            except:
                # Si falla la detección y no se permite sin rostro, retornar None
                if not allow_no_face:
                    return None
        
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
    
    def remove_background(self, image):
        """
        Elimina el fondo de la imagen usando segmentación basada en GrabCut
        
        Args:
            image: Imagen en formato BGR
            
        Returns:
            Imagen con fondo eliminado (fondo en negro)
        """
        # Crear máscara inicial (asumimos que el centro de la imagen es la persona)
        mask = np.zeros(image.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        
        # Definir rectángulo inicial (centro de la imagen)
        h, w = image.shape[:2]
        rect = (int(w*0.1), int(h*0.1), int(w*0.8), int(h*0.8))
        
        try:
            cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            result = image * mask2[:, :, np.newaxis]
            return result
        except:
            # Si falla, retornar imagen original
            return image
    
    def preprocess_for_training(self, image_path, apply_filters=True, detect_face=False, remove_bg=False):
        """
        Preprocesa una imagen desde archivo para entrenamiento
        
        Args:
            image_path: Ruta a la imagen
            apply_filters: Si True, aplica filtros
            detect_face: Si True, intenta detectar y recortar rostro (solo para humanos)
            remove_bg: Si True, elimina el fondo antes de procesar
            
        Returns:
            Array numpy con la imagen preprocesada, o None si falla
        """
        try:
            image = cv2.imread(str(image_path))
            if image is None:
                return None
            if image.size == 0:
                return None
            
            # Eliminar fondo si se solicita
            if remove_bg:
                try:
                    image = self.remove_background(image)
                except Exception:
                    pass  # Continuar sin eliminar fondo si falla
            
            # Intentar detectar rostro si se solicita (solo para humanos)
            if detect_face:
                try:
                    face_coords = self.detect_face(image)
                    if face_coords is not None:
                        x, y, w, h = face_coords
                        # Recortar el rostro con un margen
                        margin = 20
                        x = max(0, x - margin)
                        y = max(0, y - margin)
                        w = min(image.shape[1] - x, w + 2 * margin)
                        h = min(image.shape[0] - y, h + 2 * margin)
                        image = image[y:y+h, x:x+w]
                        if image.size == 0:
                            return None
                except Exception:
                    # Si falla la detección, continuar con la imagen completa
                    pass
            
            # Procesar la imagen (con o sin rostro detectado)
            # Convertir a escala de grises
            gray = self.to_grayscale(image)
            
            if apply_filters:
                try:
                    gray = self.apply_bilateral_filter(gray)
                    gray = self.apply_histogram_equalization(gray)
                except Exception:
                    pass  # Continuar sin filtros si fallan
            
            # Redimensionar
            resized = self.resize(gray)
            
            # Normalizar
            processed = self.normalize(resized)
            
            if processed is None:
                return None
            if processed.size == 0:
                return None
            
            # Aplanar para el modelo
            return processed.flatten()
        except Exception as e:
            # Cualquier error, retornar None
            return None

