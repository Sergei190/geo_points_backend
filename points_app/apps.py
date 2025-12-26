from django.apps import AppConfig

class GeoApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'points_app'
    verbose_name = 'API для работы с географическими объектами'