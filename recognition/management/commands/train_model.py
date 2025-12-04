"""
Comando de Django para entrenar el modelo desde la línea de comandos
Uso: python manage.py train_model
"""
from django.core.management.base import BaseCommand
from recognition.training import ModelTrainer
from django.conf import settings


class Command(BaseCommand):
    help = 'Entrena los modelos PCA+SVM y TensorFlow'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pca-svm-only',
            action='store_true',
            help='Entrenar solo PCA+SVM',
        )
        parser.add_argument(
            '--tensorflow-only',
            action='store_true',
            help='Entrenar solo TensorFlow',
        )
        parser.add_argument(
            '--pca-components',
            type=float,
            default=0.95,
            help='Número de componentes PCA o proporción de varianza (default: 0.95)',
        )
        parser.add_argument(
            '--epochs',
            type=int,
            default=50,
            help='Número de épocas para TensorFlow (default: 50)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando entrenamiento...'))
        
        use_pca_svm = not options['tensorflow_only']
        use_tensorflow = not options['pca_svm_only']
        
        trainer = ModelTrainer(
            model_dir=settings.MODEL_DIR,
            dataset_dir=settings.DATASET_DIR
        )
        
        try:
            results = trainer.train_all(
                use_pca_svm=use_pca_svm,
                use_tensorflow=use_tensorflow,
                pca_components=options['pca_components'],
                epochs=options['epochs']
            )
            
            self.stdout.write(self.style.SUCCESS('\n✅ Entrenamiento completado!'))
            self.stdout.write('\n📊 Resultados:')
            
            if 'pca_svm' in results:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'   PCA+SVM Accuracy: {results["pca_svm"]:.2%}'
                    )
                )
            
            if 'tensorflow' in results:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'   TensorFlow Accuracy: {results["tensorflow"]:.2%}'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error durante el entrenamiento: {str(e)}')
            )
            raise

