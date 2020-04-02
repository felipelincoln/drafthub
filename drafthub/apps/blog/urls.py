from django.urls import path, include
from .views import BlogView, PostCreateView

urlpatterns = [
    path('blog/<str:username>/', BlogView.as_view(), name='blog'),
    path('blog/<str:username>/', 
        include('drafthub.apps.post.urls')),
    path('new/', PostCreateView.as_view(), name='new')
]
