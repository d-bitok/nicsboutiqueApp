from django.apps import AppConfig


class BoutiqueappConfig(AppConfig):
    name = 'boutiqueApp'

    def ready(self):
        import boutiqueApp.signals
