from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('blog', 'github_url', 'title', 'slug', 'published_at')
    readonly_fields = ('slug', 'published_at')

    list_display = ('blog', 'title', 'slug', 'published_at',)
    list_filter = ('blog', 'published_at')
