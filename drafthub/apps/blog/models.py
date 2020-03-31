from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
