from django.apps import AppConfig

class PetappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PetApp'

    def ready(self):
        import PetApp.signals  # This is correctly indented now

