from django.urls import path
from .views import (
    BlogListView, DraftDetailView, DraftCreateView, DraftUpdateView,
    DraftDeleteView, LikeRedirectView, FavoriteRedirectView,
    CommentCreateView, CommentEditView, CommentDeleteView, TagListView
)


urlpatterns = [
    path('new/', DraftCreateView.as_view(), name='new'),
    path('tag/<str:tag>/', TagListView.as_view(), name='tag'),
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
    path('<str:username>/<slug:slug>/like/',
         LikeRedirectView.as_view(),
         name='like'),
    path('<str:username>/<slug:slug>/favorite/',
         FavoriteRedirectView.as_view(),
         name='favorite'),
    path('<str:username>/<slug:slug>/comment/',
         CommentCreateView.as_view(),
         name='comment'),
    path('<str:username>/<slug:slug>/comment/<int:pk>/edit/',
         CommentEditView.as_view(),
         name='comment-edit'),
    path('<str:username>/<slug:slug>/comment/<int:pk>/delete/',
         CommentDeleteView.as_view(),
         name='comment-delete'),
]
