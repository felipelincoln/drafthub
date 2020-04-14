from django.urls import path
from .views import (
    BlogListView, DraftDetailView, DraftCreateView, DraftUpdateView,
    DraftDeleteView,
)


urlpatterns = [
    path('new/', DraftCreateView.as_view(), name='new'),
    path('<str:username>/', BlogListView.as_view(), name='blog'),
    path('<str:username>/<slug:slug>/',
         DraftDetailView.as_view(),
         name='draft'),
    path('<str:username>/<slug:slug>/edit/',
         DraftUpdateView.as_view(),
         name='edit'),
    path('<str:username>/<slug:slug>/delete/',
         DraftDeleteView.as_view(),
         name='delete'),
]
