from django.urls import path, include
from .views import HomeView, logout_view


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logout/', logout_view, name='logout'),
]
