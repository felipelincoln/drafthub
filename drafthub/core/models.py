from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models


class Blog(AbstractUser):
    def __str__(self):
        return self.username

    def get_absolute_url(self):
        args = (self.username,)
        return reverse('blog', args=args)


    class Meta(AbstractUser.Meta):
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

