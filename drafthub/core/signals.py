from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from drafthub.blog.models import Blog
from social_django.models import Nonce, UserSocialAuth


@receiver(post_save, sender=User)
def give_new_users_a_blog(sender, instance, created, **kwargs):
    if created:
        instance.blog = Blog.objects.create(author=instance)

@receiver(post_save, sender=UserSocialAuth)
def update_username(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        github_username = instance.extra_data['login']
        drafthub_username = user.username
        if github_username != drafthub_username:
            user.username = github_username
            user.save()
