from django.apps import AppConfig

model, scaler = None, None


class LearningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'learning'

    def ready(self):
        from learning.training import load_model_and_scaler
        # Inicializa el modelo y el escalador al arrancar la aplicación
        global model, scaler
        if model is None or scaler is None:
            model, scaler = load_model_and_scaler()
