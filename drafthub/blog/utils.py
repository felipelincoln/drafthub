import random
import string
from django.utils.text import slugify

UNIQUE_LENGTH = 6
CHAR_STRING = string.ascii_lowercase + string.digits


def generate_random_string(chars=CHAR_STRING, size=UNIQUE_LENGTH):
    return ''.join(random.choice(chars) for _ in range(size))

def set_post_unique_slug(instance):
    max_length = instance._meta.get_field('slug').max_length
    post_author = instance.blog.author.username
    non_unique_slug = slugify(instance.title)
    non_unique_slug = non_unique_slug[: max_length - UNIQUE_LENGTH - 1]

    if non_unique_slug.endswith('-'):
        non_unique_slug = non_unique_slug[:-1]

    slug = non_unique_slug
    Post = instance.__class__
    while Post.objects.filter(slug=slug, blog__author__username=post_author):
        unique = generate_random_string()
        slug = non_unique_slug + '-' + unique

    return slug
