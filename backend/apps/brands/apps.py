from django.apps import AppConfig


class BrandsConfig(AppConfig):
    name = 'apps.brands'

    def ready(self):
        import apps.brands.signals
