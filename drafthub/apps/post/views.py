from django.shortcuts import render
from django.views.generic import DetailView
from drafthub.apps.post.models import Post


class PostView(DetailView):
    model = Post
    template_name = 'post/post.html'

    def get_queryset(self):
        return self.model.objects.filter(
            blog__author__username=self.kwargs['username'])
