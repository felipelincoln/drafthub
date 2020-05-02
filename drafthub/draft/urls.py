from django.urls import path
from .views import (
    DraftCreateView, DraftDetailView, DraftUpdateView, DraftDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    LikeRedirectView,
    FavoriteRedirectView,
    TagListView,
)


urlpatterns = [
    path('new/', DraftCreateView.as_view(), name='draft-new'),
    path('<str:username>/<slug:slug>/',
         DraftDetailView.as_view(),
         name='draft'),

    path('<str:username>/<slug:slug>/edit/',
         DraftUpdateView.as_view(),
         name='draft-edit'),

    path('<str:username>/<slug:slug>/delete/',
         DraftDeleteView.as_view(),
         name='draft-delete'),

    path('<str:username>/<slug:slug>/comment/new/',
         CommentCreateView.as_view(),
         name='comment-new'),

    path('<str:username>/<slug:slug>/comment/<int:pk>/edit/',
         CommentUpdateView.as_view(),
         name='comment-edit'),

    path('<str:username>/<slug:slug>/comment/<int:pk>/delete/',
         CommentDeleteView.as_view(),
         name='comment-delete'),

    path('<str:username>/<slug:slug>/like/',
         LikeRedirectView.as_view(),
         name='like'),

    path('<str:username>/<slug:slug>/favorite/',
         FavoriteRedirectView.as_view(),
         name='favorite'),

    path('tag/<str:tag>/', TagListView.as_view(), name='tag'),
]
