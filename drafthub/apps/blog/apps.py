from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'drafthub.apps.blog'

    def ready(self):
        import drafthub.apps.blog.signals
