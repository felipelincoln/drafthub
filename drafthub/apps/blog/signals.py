from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Blog


@receiver(post_save, sender=User)
def give_new_users_a_blog(sender, instance, created, **kwargs):
    if instance and created:
        instance.blog = Blog.objects.create(author=instance)
