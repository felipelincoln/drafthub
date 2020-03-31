from django.db import models
from drafthub.apps.blog.models import Blog


class Post(models.Model):
    url = models.URLField(max_length=1100)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
