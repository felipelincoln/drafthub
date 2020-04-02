import random
import string
from django.utils.text import slugify
from drafthub.apps.post.models import Post

MAXIMUM_SLUG_LENGTH = 255
UNIQUE_LENGTH = 6
DEFAULT_CHAR_STRING = string.ascii_lowercase + string.digits


def generate_random_string(chars=DEFAULT_CHAR_STRING, size=6):
    return ''.join(random.choice(chars) for _ in range(size))

def set_post_unique_slug(instance):
    if instance:
        post_author = instance.blog.author.username
        non_unique_slug = slugify(instance.title)
        non_unique_slug = non_unique_slug[:MAXIMUM_SLUG_LENGTH - UNIQUE_LENGTH - 1]

        if non_unique_slug.endswith('-'):
            non_unique_slug = non_unique_slug[:-1]

        slug = non_unique_slug
        while Post.objects.filter(slug=slug, blog__author__username=post_author):
            unique = generate_random_string(size=UNIQUE_LENGTH)
            slug = non_unique_slug + '-' + unique

        instance.slug = slug
