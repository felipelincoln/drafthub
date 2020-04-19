from django.contrib import admin
from .models import Draft


@admin.register(Draft)
class PostAdmin(admin.ModelAdmin):
    fields = ('blog', 'github_url', 'title', 'abstract', 'slug', 'pub_date', 'last_update')
    readonly_fields = ('slug', 'pub_date', 'last_update')

    list_display = ('blog', 'title', 'slug', 'pub_date', 'last_update')
    list_filter = ('blog', 'pub_date', 'last_update')
