from django.urls import path, include

from .views import (
    DraftCreateView, DraftDetailView, DraftUpdateView, DraftDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    LikeRedirectView,
    FavoriteRedirectView,
    TagListView,
)


draft_urlpatterns = [
    path('',DraftDetailView.as_view(),name='draft'),
    path('edit/', DraftUpdateView.as_view(), name='draft-edit'),
    path('delete/', DraftDeleteView.as_view(), name='draft-delete'),
    path('comment/new/', CommentCreateView.as_view(), name='comment-new'),
    path('comment/<int:pk>/edit/',
         CommentUpdateView.as_view(),
         name='comment-edit'),
    path('comment/<int:pk>/delete/',
         CommentDeleteView.as_view(),
         name='comment-delete'),
    path('like/', LikeRedirectView.as_view(), name='draft-like'),
    path('favorite/', FavoriteRedirectView.as_view(), name='draft-favorite'),
]

urlpatterns = [
    path('new/', DraftCreateView.as_view(), name='new'),
    path('tag/<str:tag>/', TagListView.as_view(), name='tag'),
    path('blog/<str:blog>/<slug:slug>/', include(draft_urlpatterns))
]
