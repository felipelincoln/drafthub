from django.db import models
from drafthub.apps.blog.models import Blog
import requests


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    raw_content_url = models.URLField(max_length=1100)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,
                            editable=False,)

    def __str__(self):
        return self.title

    @property
    def get_github_content(self):
        raw_content = requests.get(self.raw_content_url)
        return raw_content.text
