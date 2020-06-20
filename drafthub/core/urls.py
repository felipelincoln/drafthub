from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    BlogListView, BlogUpdateView,
    HomeView, LoginView, SearchListView,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchListView.as_view(), name='search'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('settings/', BlogUpdateView.as_view(), name='edit'),
    path('<str:blog>/', BlogListView.as_view(), name='blog'),
]
