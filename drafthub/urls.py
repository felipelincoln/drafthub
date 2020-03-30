from django.contrib import admin
from django.urls import path, include

from drafthub.apps.core.views import HomeView, logout_view # provisional

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls'), name='social'),
    path('', HomeView.as_view(), name='home'), # provisional
    path('logout/', logout_view, name='logout'), # provisional
]
