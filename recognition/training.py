"""
Módulo de entrenamiento del modelo
Utiliza PCA, SVM y TensorFlow
"""
import os
import numpy as np
import joblib
import cv2
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import tensorflow as tf
# Usar tf.keras para compatibilidad con todas las versiones
keras = tf.keras
layers = tf.keras.layers
from pathlib import Path
from .preprocessing import ImagePreprocessor


class ModelTrainer:
    """Clase para entrenar modelos de reconocimiento de rostros"""
    
    def __init__(self, model_dir='models', dataset_dir='dataset'):
        """
        Args:
            model_dir: Directorio donde se guardan los modelos
            dataset_dir: Directorio del dataset
        """
        self.model_dir = Path(model_dir)
        self.dataset_dir = Path(dataset_dir)
        self.model_dir.mkdir(exist_ok=True)
        
        self.preprocessor = ImagePreprocessor()
        self.scaler = StandardScaler()
        self.pca = None
        self.svm = None
        self.tf_model = None
        
    def load_dataset(self):
        """
        Carga el dataset desde las carpetas 'human' y 'non_human'
        
        Returns:
            X: Array de características (n_samples, n_features)
            y: Array de etiquetas (0 = no humano, 1 = humano)
        """
        X = []
        y = []
        
        # Cargar imágenes humanas (etiqueta 1) - necesita detectar rostros
        human_dir = self.dataset_dir / 'human'
        human_loaded = 0
        human_failed = 0
        if human_dir.exists():
            print(f"📁 Cargando imágenes humanas de {human_dir}...")
            img_files = list(human_dir.glob('*.jpg')) + list(human_dir.glob('*.png')) + list(human_dir.glob('*.jpeg'))
            print(f"   Encontradas {len(img_files)} imágenes")
            for img_file in img_files:
                # Procesar imagen humana: intentar detectar rostro, pero si falla procesar imagen completa
                processed = self.preprocessor.preprocess_for_training(
                    str(img_file), 
                    apply_filters=True, 
                    detect_face=True,  # Intentar detectar rostro
                    remove_bg=False
                )
                
                if processed is not None:
                    X.append(processed)
                    y.append(1)
                    human_loaded += 1
                else:
                    human_failed += 1
            print(f"   ✅ Cargadas: {human_loaded}, ❌ Error al procesar: {human_failed}")
        else:
            print(f"⚠️ Carpeta 'human' no existe")
        
        # Cargar imágenes no humanas (etiqueta 0) - NO necesita detectar rostros
        non_human_dir = self.dataset_dir / 'non_human'
        non_human_loaded = 0
        non_human_failed = 0
        if non_human_dir.exists():
            print(f"📁 Cargando imágenes no humanas de {non_human_dir}...")
            img_files = list(non_human_dir.glob('*.jpg')) + list(non_human_dir.glob('*.png')) + list(non_human_dir.glob('*.jpeg'))
            print(f"   Encontradas {len(img_files)} imágenes")
            for img_file in img_files:
                # Procesar imagen no humana: NO detectar rostros, procesar imagen completa directamente
                processed = self.preprocessor.preprocess_for_training(
                    str(img_file), 
                    apply_filters=True, 
                    detect_face=False,  # NO detectar rostros para objetos
                    remove_bg=False
                )
                
                if processed is not None:
                    X.append(processed)
                    y.append(0)
                    non_human_loaded += 1
                else:
                    non_human_failed += 1
            print(f"   ✅ Cargadas: {non_human_loaded}, ❌ Error al procesar: {non_human_failed}")
        else:
            print(f"⚠️ Carpeta 'non_human' no existe")
        
        if len(X) == 0:
            error_msg = "No se encontraron imágenes válidas en el dataset.\n"
            error_msg += f"Humanas: {human_loaded} cargadas, {human_failed} sin rostro detectado\n"
            error_msg += f"No humanas: {non_human_loaded} cargadas, {non_human_failed} con error\n"
            error_msg += "Asegúrate de tener carpetas 'human' y 'non_human' con imágenes válidas."
            raise ValueError(error_msg)
        
        # Advertencia si falta una categoría
        if human_loaded > 0 and non_human_loaded == 0:
            print("\n❌ ERROR: Solo se encontraron imágenes humanas.")
            print("   El modelo requiere imágenes de AMBAS categorías para entrenar.")
            print("   Por favor, agrega imágenes no humanas en 'dataset/non_human/'")
            print("   Se recomienda al menos 20-30 imágenes no humanas.\n")
        elif human_loaded == 0 and non_human_loaded > 0:
            print("\n❌ ERROR: Solo se encontraron imágenes no humanas.")
            print("   El modelo requiere imágenes de AMBAS categorías para entrenar.")
            print("   Por favor, agrega imágenes humanas en 'dataset/human/'")
            print("   Se recomienda al menos 20-30 imágenes humanas.\n")
        
        # Verificar que haya suficientes muestras
        if len(X) < 10:
            print(f"\n⚠️ ADVERTENCIA: Solo {len(X)} muestras disponibles.")
            print("   Se recomienda tener al menos 20-30 muestras para un entrenamiento adecuado.\n")
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"✅ Dataset cargado: {len(X)} muestras")
        print(f"   - Humanos: {np.sum(y == 1)}")
        print(f"   - No humanos: {np.sum(y == 0)}")
        
        return X, y
    
    def train_pca_svm(self, X, y, pca_components=0.95, test_size=0.2):
        """
        Entrena un modelo PCA + SVM
        
        Args:
            X: Características
            y: Etiquetas
            pca_components: Número de componentes PCA (o proporción de varianza si < 1)
            test_size: Proporción de datos para test
            
        Returns:
            accuracy: Precisión del modelo
        """
        print("\n🔧 Entrenando modelo PCA + SVM...")
        
        # Verificar que haya al menos 2 clases para SVM
        unique_classes = np.unique(y)
        if len(unique_classes) < 2:
            raise ValueError(
                f"Se requiere al menos 2 clases para entrenar el modelo. "
                f"Encontradas: {len(unique_classes)} clase(s). "
                f"Por favor, agrega imágenes en ambas carpetas 'human' y 'non_human'."
            )
        
        # Verificar si hay múltiples clases para stratify
        use_stratify = len(unique_classes) > 1 and all(np.sum(y == cls) >= 2 for cls in unique_classes)
        
        # Dividir en train y test
        if use_stratify:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
        else:
            print("⚠️ No se puede usar stratify (clases con menos de 2 muestras)")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
        
        # Normalización
        print("📊 Normalizando datos...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # PCA
        print(f"🔍 Aplicando PCA (componentes: {pca_components})...")
        self.pca = PCA(n_components=pca_components, svd_solver='auto')
        X_train_pca = self.pca.fit_transform(X_train_scaled)
        X_test_pca = self.pca.transform(X_test_scaled)
        
        print(f"   Componentes PCA: {self.pca.n_components_}")
        print(f"   Varianza explicada: {self.pca.explained_variance_ratio_.sum():.2%}")
        
        # SVM
        print("🤖 Entrenando SVM...")
        self.svm = SVC(kernel='rbf', probability=True, random_state=42)
        self.svm.fit(X_train_pca, y_train)
        
        # Evaluación
        y_pred = self.svm.predict(X_test_pca)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n📈 Resultados PCA + SVM:")
        print(f"   Accuracy: {accuracy:.2%}")
        print("\n📋 Reporte de clasificación:")
        # Manejar nombres de clases dinámicamente
        class_names = ['No Humano', 'Humano'] if len(unique_classes) == 2 else [f'Clase {cls}' for cls in unique_classes]
        print(classification_report(y_test, y_pred, target_names=class_names))
        
        # Guardar modelos
        joblib.dump(self.scaler, self.model_dir / 'scaler.pkl')
        joblib.dump(self.pca, self.model_dir / 'pca_model.pkl')
        joblib.dump(self.svm, self.model_dir / 'svm_model.pkl')
        
        print(f"\n💾 Modelos guardados en {self.model_dir}")
        
        return accuracy
    
    def train_tensorflow(self, X, y, test_size=0.2, epochs=50, batch_size=32):
        """
        Entrena un modelo de TensorFlow/Keras
        
        Args:
            X: Características
            y: Etiquetas
            test_size: Proporción de datos para test
            epochs: Número de épocas
            batch_size: Tamaño del batch
            
        Returns:
            accuracy: Precisión del modelo
        """
        print("\n🔧 Entrenando modelo TensorFlow...")
        
        # Verificar que haya al menos 2 clases para TensorFlow
        unique_classes = np.unique(y)
        if len(unique_classes) < 2:
            raise ValueError(
                f"Se requiere al menos 2 clases para entrenar el modelo. "
                f"Encontradas: {len(unique_classes)} clase(s). "
                f"Por favor, agrega imágenes en ambas carpetas 'human' y 'non_human'."
            )
        
        # Verificar si hay múltiples clases para stratify
        use_stratify = len(unique_classes) > 1 and all(np.sum(y == cls) >= 2 for cls in unique_classes)
        
        # Dividir en train y test
        if use_stratify:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
        else:
            print("⚠️ No se puede usar stratify (clases con menos de 2 muestras)")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
        
        # Redimensionar para CNN (asumiendo imágenes de 160x160)
        img_size = int(np.sqrt(X.shape[1]))
        X_train_reshaped = X_train.reshape(-1, img_size, img_size, 1)
        X_test_reshaped = X_test.reshape(-1, img_size, img_size, 1)
        
        # Normalizar
        X_train_reshaped = X_train_reshaped.astype('float32')
        X_test_reshaped = X_test_reshaped.astype('float32')
        
        # Construir modelo CNN
        model = keras.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_size, img_size, 1)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        print("📊 Arquitectura del modelo:")
        model.summary()
        
        # Callbacks
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        # Entrenar
        print(f"\n🏋️ Entrenando por {epochs} épocas...")
        history = model.fit(
            X_train_reshaped, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(X_test_reshaped, y_test),
            callbacks=[early_stopping],
            verbose=1
        )
        
        # Evaluación
        test_loss, test_accuracy = model.evaluate(X_test_reshaped, y_test, verbose=0)
        
        print(f"\n📈 Resultados TensorFlow:")
        print(f"   Accuracy: {test_accuracy:.2%}")
        
        # Guardar modelo
        model_path = self.model_dir / 'tensorflow_model.h5'
        model.save(model_path)
        self.tf_model = model
        
        print(f"\n💾 Modelo guardado en {model_path}")
        
        return test_accuracy
    
    def train_all(self, use_pca_svm=True, use_tensorflow=True, **kwargs):
        """
        Entrena todos los modelos configurados
        
        Args:
            use_pca_svm: Si True, entrena PCA+SVM
            use_tensorflow: Si True, entrena TensorFlow
            **kwargs: Argumentos adicionales para los métodos de entrenamiento
            
        Returns:
            dict: Diccionario con los resultados de cada modelo
        """
        # Cargar dataset
        X, y = self.load_dataset()
        
        results = {}
        
        # Entrenar PCA + SVM
        if use_pca_svm:
            pca_components = kwargs.get('pca_components', 0.95)
            test_size = kwargs.get('test_size', 0.2)
            results['pca_svm'] = self.train_pca_svm(X, y, pca_components, test_size)
        
        # Entrenar TensorFlow
        if use_tensorflow:
            epochs = kwargs.get('epochs', 50)
            batch_size = kwargs.get('batch_size', 32)
            results['tensorflow'] = self.train_tensorflow(X, y, test_size, epochs, batch_size)
        
        return results

