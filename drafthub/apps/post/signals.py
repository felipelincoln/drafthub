from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from drafthub.apps.core.utils import generate_random_string
from .models import Post


@receiver(pre_save, sender=Post)
def add_unique_slug(sender, instance, *args, **kwargs):
    MAXIMUM_SLUG_LENGTH = 255
    UNIQUE_LENGTH = 6

    if instance:
        post_author = instance.blog.author.username
        non_unique_slug = slugify(instance.title)
        non_unique_slug = non_unique_slug[:MAXIMUM_SLUG_LENGTH - UNIQUE_LENGTH - 1]

        if non_unique_slug.endswith('-'):
            non_unique_slug = non_unique_slug[:-1]

        slug = non_unique_slug
        while Post.objects.filter(slug=slug, blog__author__username=post_author):
            unique = generate_random_string()
            slug = non_unique_slug + '-' + unique

        instance.slug = slug
