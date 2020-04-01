from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('blog', 'raw_content_url', 'title', 'slug',)
    readonly_fields = ('slug',)

    list_display = ('blog', 'title',)
    list_filter = ('blog',)
