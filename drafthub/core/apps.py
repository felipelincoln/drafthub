from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'drafthub.core'

    def ready(self):
        import drafthub.core.signals
