from django.apps import AppConfig

class AutoWaterSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auto_water_system_app'

    def ready(self):
        import auto_water_system_app.signals  