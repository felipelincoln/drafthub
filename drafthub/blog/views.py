from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from .models import Blog, Post


class BlogView(ListView):
    paginate_by = 5
    model = Post

    def get_queryset(self):
        return self.model.objects.filter(
            blog__author__username=self.kwargs['username'])


class PostView(DetailView):
    model = Post

    def get_queryset(self):
        return self.model.objects.filter(
            blog__author__username=self.kwargs['username'])


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['github_url', 'title',]

    def form_valid(self, form):
        form.instance.blog = self.request.user.blog
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['github_url', 'title',]

    def get_queryset(self):
        return self.model.objects.filter(
            blog__author__username=self.kwargs['username'])

    def user_has_access(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return request.user == self.object.blog.author
        return redirect_to_login(request.get_full_path())

    def dispatch(self, request, *args, **kwargs):
        if not self.user_has_access(request):
            return redirect(self.object)
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_queryset(self):
        return self.model.objects.filter(
            blog__author__username=self.kwargs['username'])

    def user_has_access(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return request.user == self.object.blog.author
        return redirect_to_login(request.get_full_path())

    def dispatch(self, request, *args, **kwargs):
        if not self.user_has_access(request):
            return redirect(self.object)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        args = (self.kwargs['username'],)
        return reverse_lazy('blog', args=args)
