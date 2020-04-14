from django.contrib import admin
from .models import Draft


@admin.register(Draft)
class PostAdmin(admin.ModelAdmin):
    fields = ('blog', 'github_url', 'title', 'slug', 'pub_date',)
    readonly_fields = ('slug', 'pub_date',)

    list_display = ('blog', 'title', 'slug', 'pub_date',)
    list_filter = ('blog', 'pub_date',)
