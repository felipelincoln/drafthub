from django.contrib import admin
from django.urls import path, include

from drafthub.apps.core.views import Home # provisional

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls'), name='social'),
    path('', Home.as_view(), name='home'), # provisional
]
