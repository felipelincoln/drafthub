"""Url config for drafthub"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import (
    error404_view, error500_view, error403csrf_view, error400_view
)


handler404 = error404_view
handler500 = error500_view
handler400 = error400_view

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include('social_django.urls'), name='social'),
    path('', include('drafthub.draft.urls')),
    path('', include('drafthub.core.urls')),
]
