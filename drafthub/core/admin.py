from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from social_django.models import Nonce, Association

from .forms import BlogCreationForm, BlogChangeForm


Blog = get_user_model()

admin.site.site_header = 'DraftHub admin panel'
admin.site.unregister(Group)
admin.site.unregister(Nonce)
admin.site.unregister(Association)


@admin.register(Blog)
class MyUserAdmin(UserAdmin):
    add_form = BlogCreationForm
    form = BlogChangeForm
    model = Blog

    fieldsets = (
        (None,{
            'fields': ('username', 'password','last_login',
                       'date_joined'),
        }),
        ('Status',{
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined')
    list_filter = ('is_active', 'date_joined', 'last_login')
    list_display = ('username', 'last_login', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
