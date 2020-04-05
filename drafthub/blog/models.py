from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Blog(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username

    def get_absolute_url(self):
        args = (self.author.username,)
        return reverse('blog', args=args)


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    github_url = models.CharField(max_length=1100)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from .utils import get_post_unique_slug
            self.slug = get_post_unique_slug(self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'username': self.blog.author.username,
            'slug': self.slug,
        }
        return reverse('post', kwargs=kwargs)

    class Meta:
        ordering = ['-pub_date',]
