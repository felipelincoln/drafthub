from django.contrib import admin
from django.urls import path, include

from drafthub.apps.core.views import HomeView, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls'), name='social'),
    path('', HomeView.as_view(), name='home'),
    path('logout/', logout_view, name='logout'),
]
