from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include('social_django.urls'), name='social'),
    path('', include('drafthub.draft.urls')),
    path('', include('drafthub.core.urls')),
]
