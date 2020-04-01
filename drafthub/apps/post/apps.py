from django.apps import AppConfig


class PostConfig(AppConfig):
    name = 'drafthub.apps.post'

    def ready(self):
        import drafthub.apps.post.signals
