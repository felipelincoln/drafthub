from django.urls import path
from .views import PostView


urlpatterns = [
    path('<slug:slug>/', PostView.as_view(), name='post'),
]
