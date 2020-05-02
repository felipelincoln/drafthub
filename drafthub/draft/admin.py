from django.contrib import admin
from .models import Draft, Tag, Comment, Activity


@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):

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

    def short_title(self, obj):
        return obj.get_short_title(25)

    def short_slug(self, obj):
        short = obj.slug
        if len(short) > 25:
            short = short[:22]
            short = short.rstrip()
            short = short + '...'

        return short


    fieldsets = (
        (None, {
            'fields': (
                'blog', 'github_url', 'title', 'slug', 'abstract', 'pub_date',
                'last_update', 'tags',
            ),
        }),
        ('Activities', {
            'fields': (
                'hits', 'last_views', 'last_favorites', 'last_likes', 'views',
                'favorites', 'likes',
            ),
        }),
    )
    readonly_fields = (
        'hits', 'slug', 'pub_date', 'last_update', 'last_views',
        'last_favorites', 'last_likes', 'views', 'favorites', 'likes',
    )
    list_display = (
        'blog', 'short_title', 'short_slug', 'pub_date',
        'last_update', 'hits',
    )
    list_filter = ('pub_date', 'last_update', 'blog', 'tags')


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
