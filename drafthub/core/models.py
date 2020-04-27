from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Blog(AbstractUser):
    bio = models.TextField(max_length=160, default='get_from_github')

    def __str__(self):
        return self.username

    @property
    def favorited_drafts(self):
        Draft = self.my_drafts.model
        return Draft.objects.filter(
            activities__blog=self,
            activities__favorited__isnull=False
        )

    @property
    def liked_drafts(self):
        Draft = self.my_drafts.model
        return Draft.objects.filter(
            activities__blog=self,
            activities__liked__isnull=False
        )

    @property
    def viewed_drafts(self):
        Draft = self.my_drafts.model
        return Draft.objects.filter(
            activities__blog=self,
            activities__viewed__isnull=False
        )

    def get_absolute_url(self):
        args = (self.username,)
        return reverse('blog', args=args)


    class Meta(AbstractUser.Meta):
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

