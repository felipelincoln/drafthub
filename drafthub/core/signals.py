from django.db.models.signals import post_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth


@receiver(post_save, sender=UserSocialAuth)
def update_username(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        github_username = instance.extra_data['login']
        drafthub_username = user.username
        if github_username != drafthub_username:
            user.username = github_username
            user.save()
