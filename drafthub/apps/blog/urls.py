from django.urls import path, include
from .views import BlogView, NewPostView

urlpatterns = [
    path('new/', NewPostView.as_view(), name='new'),
    path('blog/<str:username>/', BlogView.as_view(), name='blog'),
    path('blog/<str:username>/', 
        include('drafthub.apps.post.urls')),
]
#    path('<str:username>/<slug:slug>/',
#        include('drafthub.apps.post.urls')),
