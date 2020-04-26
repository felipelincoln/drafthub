from django import forms
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from .managers import DraftManager, TagManager

Blog = get_user_model()

class Draft(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='my_drafts')
    tags = models.ManyToManyField('draft.tag', related_name='tagged_drafts')
    comments = models.ManyToManyField('draft.comment', related_name='draft')
    likes = models.ManyToManyField(Blog, related_name='likes')

    github_url = models.URLField(max_length=1100)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    abstract = models.TextField(max_length=255, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(blank=True, null=True)
    view_count = models.IntegerField(default=0)

    objects = DraftManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'username': self.blog.username,
            'slug': self.slug,
        }
        return reverse('draft', kwargs=kwargs)

    def get_short_title(self):
        short = self.title
        if len(short) > 45:
            short = short[:45]
            short = short.rstrip()
            short = short + '...'

        return short

    class Meta:
        ordering = ['-pub_date',]
        verbose_name = 'draft'
        verbose_name_plural = 'drafties'


class Tag(models.Model):
    name = models.SlugField(max_length=25)

    objects = TagManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', args=(self.name,))

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blog.username + "'s comment (#{})".format(self.id)

    def get_absolute_url(self):
        kwargs = {
            'username': self.draft.get().blog.username,
            'slug': self.draft.get().slug,
        }
        return reverse('draft', kwargs=kwargs)

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
