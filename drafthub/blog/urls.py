from django.urls import path
from .views import (
    BlogView, PostView, PostCreateView, PostUpdateView, PostDeleteView
)


urlpatterns = [
    path('new/', PostCreateView.as_view(), name='new'),
    path('<str:username>/', BlogView.as_view(), name='blog'),
    path('<str:username>/<slug:slug>/',
         PostView.as_view(),
         name='post'),
    path('<str:username>/<slug:slug>/edit/',
         PostUpdateView.as_view(),
         name='edit'),
    path('<str:username>/<slug:slug>/delete/',
         PostDeleteView.as_view(),
         name='delete'),
]
