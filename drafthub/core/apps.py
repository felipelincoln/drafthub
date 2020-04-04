from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'drafthub.core'

    def ready(self):
        import drafthub.core.signals
