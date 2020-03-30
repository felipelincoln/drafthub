from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress


admin.site.site_header = 'DraftHub admin panel'
admin.site.unregister(Group)


class MyUserAdmin(UserAdmin):
    fieldsets = (
        ('Credentials',{
            'fields': ('username', 'password'),
        }),
        ('Information',{
            'fields': ('last_login', 'date_joined'),
        }),
        ('User status',{
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined')
    list_filter = ('is_active', 'date_joined', 'last_login')
    list_display = ('username', 'last_login', 'date_joined', 'is_active', 'is_staff', 'is_superuser')


admin.site.unregister(User)
admin.site.unregister(EmailAddress)
admin.site.register(User, MyUserAdmin)
