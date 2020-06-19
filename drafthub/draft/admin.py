from django.contrib import admin

from .models import Draft, Tag, Comment, Activity
from .utils import shorten_string


@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):
    def last_activities(self, obj):
        return obj.last_activities

    last_activities.admin_order_field = 'last_activities'

    def last_views(self, obj):
        return f'{obj.last_views}\n' + ', '.join(
            [blog.username for blog in obj.views][:obj.last_views]
        )

    def last_favorites(self, obj):
        return f'{obj.last_favorites}\n' + ', '.join(
            [blog.username for blog in obj.favorites][:obj.last_favorites]
        )

    def last_likes(self, obj):
        return f'{obj.last_likes}\n' + ', '.join(
            [blog.username for blog in obj.likes][:obj.last_likes]
        )

    def views(self, obj):
        return f'{obj.views.count()}\n' + ', '.join(
            [blog.username for blog in obj.views]
        )

    def favorites(self, obj):
        return f'{obj.favorites.count()}\n' + ', '.join(
            [blog.username for blog in obj.favorites]
        )

    def likes(self, obj):
        return f'{obj.likes.count()}\n' + ', '.join(
            [blog.username for blog in obj.likes]
        )

    fieldsets = (
        (None, {
            'fields': (
                'id', 'did', 'blog', 'github_url', 'title', 'slug', 'abstract',
                'created', 'updated', 'tags',
            ),
        }),
        ('Activities', {
            'fields': (
                'last_activities', 'hits', 'last_views', 'last_likes',
                'last_favorites', 'views', 'favorites', 'likes',
            ),
        }),
    )
    readonly_fields = (
        'id', 'last_activities', 'hits', 'slug', 'created', 'updated', 'last_views',
        'last_likes', 'last_favorites', 'views', 'likes', 'favorites', 'did'
    )
    list_display = (
        'did', 'id', 'created', 'updated', 'last_activities', 'hits',
    )
    list_filter = ('created', 'updated', 'blog', 'tags')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    def drafts(self, obj):
        return f'{obj.tagged_drafts.count()}\n' + ', '.join(
            [draft.did for draft in obj.tagged_drafts.all()]
        )
    def num_drafts(self, obj):
        return obj.num_drafts

    def last_drafts(self, obj):
        return obj.last_drafts

    def last_views(self, obj):
        return f'{obj.tagged_drafts_last_views}'

    def last_favorites(self, obj):
        return f'{obj.tagged_drafts_last_favorites}'

    def last_likes(self, obj):
        return f'{obj.tagged_drafts_last_likes}'

    def tagged_drafts_last_activities(self, obj):
        return obj.tagged_drafts_last_activities

    def icon(self, obj):
        return obj.icon

    def description(self, obj):
        return obj.description

    def short_description(self, obj):
        return shorten_string(obj.description(50))
        

    tagged_drafts_last_activities.admin_order_field = \
        'tagged_drafts_last_activities'

    fieldsets = (
        (None, {
            'fields': (
                'name', 'icon', 'description', 'num_drafts', 'last_drafts',
                'drafts',
            ),
        }),
        ('Activities', {
            'fields': (
                'tagged_drafts_last_activities', 'last_views', 'last_likes',
                'last_favorites',
            ),
        }),
    )
    readonly_fields = (
        'num_drafts', 'last_drafts', 'drafts', 'tagged_drafts_last_activities',
        'last_views', 'last_likes', 'last_favorites', 'icon', 'description',
        'short_description'
    )
    list_display = (
        'name', 'description', 'num_drafts', 'last_drafts',
        'tagged_drafts_last_activities',
    )


@admin.register(Comment)
class Comment(admin.ModelAdmin):

    def short_content(self, obj):
        return shorten_string(obj.content, 50)

    list_display = (
        'blog', 'draft', 'short_content', 'created', 'updated'
    )
    list_filter = ('created', 'updated', 'blog', 'draft__did',)


@admin.register(Activity)
class Activity(admin.ModelAdmin):
    fields = ('blog', 'draft', 'viewed', 'favorited', 'liked')
    readonly_fields = ('viewed',)
    list_display = ('blog', 'draft', 'viewed', 'favorited', 'liked',)
    list_filter = ('blog', 'draft__did', 'viewed', 'favorited', 'liked',)
