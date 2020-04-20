from django.db.models.signals import post_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth


@receiver(post_save, sender=UserSocialAuth)
def update_username(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        github = instance.extra_data

        if github['login'] != user.username:
            user.username = github['login']
            user.save(update_fields=['username'])

        if not user.avatar:
            user.avatar = github['avatar_url']
            user.save(update_fields=['avatar'])
