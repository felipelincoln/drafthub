from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from .models import Blog, Post
from .forms import PostForm


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
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request

        return kwargs

    def form_valid(self, form):
        form.instance.blog = self.request.user.blog
        form.instance.slug = self.get_post_unique_slug(form.instance)

        return super().form_valid(form)

    def get_post_unique_slug(self, instance, unique_len=6):
        from django.utils.text import slugify
        from .utils import generate_random_string

        max_length = Post._meta.get_field('slug').max_length
        author = instance.blog.author.username
        non_unique_slug = slugify(instance.title)
        non_unique_slug = non_unique_slug[: max_length - unique_len - 1]

        if non_unique_slug.endswith('-'):
            non_unique_slug = non_unique_slug[:-1]

        slug = non_unique_slug
        while Post.objects.filter(slug=slug, blog__author__username=author):
            unique = generate_random_string()
            slug = non_unique_slug + '-' + unique

        return slug


class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request

        return kwargs

    def get_queryset(self):
        return Post.objects.filter(
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
