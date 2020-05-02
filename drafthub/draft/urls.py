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
    path('edit/', DraftUpdateView.as_view()),
    path('delete/', DraftDeleteView.as_view()),
    path('comment/new/', CommentCreateView.as_view()),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view()),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view()),
    path('like/', LikeRedirectView.as_view()),
    path('favorite/', FavoriteRedirectView.as_view()),
]

urlpatterns = [
    path('new/', DraftCreateView.as_view()),
    path('tag/<str:tag>/', TagListView.as_view(), name='tag'),
    path('blog/<str:username>/<slug:slug>/', include(draft_urlpatterns))
]
