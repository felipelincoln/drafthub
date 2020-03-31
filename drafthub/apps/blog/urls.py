from django.urls import path, include

urlpatterns = [
    path('<str:username>/<slug:slug>/',
        include('drafthub.apps.post.urls')),
]
