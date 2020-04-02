from django.urls import path
from .views import PostView, PostUpdateView, PostDeleteView


urlpatterns = [
    path('<slug:slug>/', PostView.as_view(), name='post'),
    path('<slug:slug>/edit/', PostUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='delete'),
]
