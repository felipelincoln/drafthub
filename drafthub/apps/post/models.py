from django.db import models
from django.urls import reverse
from drafthub.apps.blog.models import Blog
import requests


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    github_url = models.CharField(max_length=1100)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    published_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'username': self.blog.author.username,
            'slug': self.slug,
        }
        return reverse('post', kwargs=kwargs)

    @property
    def content(self):
        raw_content = requests.get(self.github_url)
        return raw_content.text


    class Meta:
        ordering = ['-published_at',]

