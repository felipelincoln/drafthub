from django.urls import path
from .views import PostView, PostUpdateView


urlpatterns = [
    path('<slug:slug>/', PostView.as_view(), name='post'),
    path('<slug:slug>/edit/', PostUpdateView.as_view(), name='edit')
]
