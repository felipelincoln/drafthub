from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Blog(AbstractUser):
    bio = models.CharField(max_length=160, default='get_from_github')
    text = models.TextField(default='say a word about your blog ;)')

    def __str__(self):
        return self.username

    @property
    def favorited_drafts(self):
        Draft = self.my_drafts.model
        return Draft.objects.filter(
            activities__blog=self,
            activities__favorited__isnull=False
        ).order_by('-activities__favorited')

    @property
    def liked_drafts(self):
        Draft = self.my_drafts.model
        return Draft.objects.filter(
            activities__blog=self,
            activities__liked__isnull=False
        ).order_by('-activities__liked')

    @property
    def viewed_drafts(self):
        Draft = self.my_drafts.model
        return Draft.objects.filter(
            activities__blog=self,
            activities__viewed__isnull=False
        ).order_by('-activities__viewed')

    def get_absolute_url(self):
        args = (self.username,)
        return reverse('blog', args=args)


    class Meta(AbstractUser.Meta):
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

