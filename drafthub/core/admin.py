from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from social_django.models import Nonce, Association


admin.site.site_header = 'DraftHub admin panel'
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.unregister(Nonce)
admin.site.unregister(Association)


@admin.register(User)
class MyUserAdmin(UserAdmin):
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
