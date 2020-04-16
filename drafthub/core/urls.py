from django.urls import path
from django.contrib.auth import views as auth_views

from .views import HomeView, LoginView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
]
