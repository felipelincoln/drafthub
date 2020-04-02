from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from drafthub.apps.post.models import Post
from drafthub.apps.core.utils import set_post_unique_slug


class BlogView(ListView):
    paginate_by = 5
    model = Post
    template_name = 'blog/blog.html'

    def get_queryset(self):
        return self.model.objects.filter(
            blog__author__username=self.kwargs['username'])


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['raw_content_url', 'title']

    def form_valid(self, form):
        form.instance.blog = self.request.user.blog
        set_post_unique_slug(form.instance)
        return super().form_valid(form)
