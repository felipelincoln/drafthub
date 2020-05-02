from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from .managers import DraftManager, TagManager

Blog = get_user_model()

class Draft(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='my_drafts',
    )
    tags = models.ManyToManyField(
        'draft.tag',
        blank=True,
        related_name='tagged_drafts',
    )

    github_url = models.URLField(max_length=1100)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=107)
    abstract = models.TextField(max_length=200, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(blank=True, null=True)
    hits = models.IntegerField(default=0)

    objects = DraftManager()

    def __str__(self):
        return self.get_short_title()

    def get_absolute_url(self):
        kwargs = {
            'username': self.blog.username,
            'slug': self.slug,
        }
        return reverse('draft', kwargs=kwargs)

    @property
    def favorites(self):
        return Blog.objects.filter(
            my_activities__draft=self,
            my_activities__favorited__isnull=False,
        )

    @property
    def likes(self):
        return Blog.objects.filter(
            my_activities__draft=self,
            my_activities__liked__isnull=False,
        )

    @property
    def views(self):
        return Blog.objects.filter(
            my_activities__draft=self,
            my_activities__viewed__isnull=False,
        )

    def get_short_title(self, max_len=50):
        short = self.title
        if len(short) > max_len:
            short = short[:max_len-3]
            short = short.rstrip()
            short = short + '...'

        return short

    class Meta:
        ordering = ['-pub_date', '-last_update']
        verbose_name = 'draft'
        verbose_name_plural = 'drafts'


class Tag(models.Model):
    name = models.SlugField(max_length=25)

    objects = TagManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', args=(self.name,))

class Comment(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='my_comments',
    )
    draft = models.ForeignKey(
        Draft,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)


    def get_absolute_url(self):
        draft_url = self.draft.get_absolute_url()
        pk = self.id
        return f'{draft_url}#{pk}'

    class Meta:
        ordering = ['created',]
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


class Activity(models.Model):
    blog = models.ForeignKey(
        Blog, 
        on_delete=models.CASCADE,
        related_name='my_activities'
    )
    draft = models.ForeignKey(
        Draft,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    favorited = models.DateTimeField(blank=True, null=True)
    liked = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return str(self.blog) + ' -> ' + str(self.draft)


    class Meta:
        verbose_name = 'activity'
        verbose_name_plural = 'activities'
