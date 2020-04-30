from django.contrib import admin
from .models import Draft, Tag, Comment, Activity


@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):
    fields = (
        'blog', 'github_url', 'title', 'hits', 'abstract', 'tags',
        'slug', 'pub_date', 'last_update', 'comments'
    )
    readonly_fields = ('hits', 'slug', 'pub_date', 'last_update', )
    list_display = (
        'blog', 'title', 'hits', 'slug', 'pub_date',
        'last_update'
    )
    list_filter = ('blog', 'pub_date', 'last_update', 'hits', 'tags')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    pass


@admin.register(Activity)
class Activity(admin.ModelAdmin):
    fields = (
        'blog', 'draft', 'favorited', 'liked', 'viewed',
    )
    readonly_fields = ('viewed',)
    list_display = ('blog', 'draft', 'favorited', 'liked', 'viewed',)
    list_filter = ('blog', 'draft', 'favorited', 'liked', 'viewed',)
