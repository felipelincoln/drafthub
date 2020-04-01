from django.urls import path, include
from .views import BlogView, new_post_view

urlpatterns = [
    path('new/', new_post_view, name='new'),
    path('blog/<str:username>/', BlogView.as_view(), name='blog'),
    path('blog/<str:username>/', 
        include('drafthub.apps.post.urls')),
]
