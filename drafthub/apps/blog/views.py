from django.views.generic import TemplateView, ListView
from drafthub.apps.post.models import Post

class BlogView(ListView):
    paginate_by = 5
    model = Post
    template_name = 'blog/blog.html'

    def get_queryset(self):
        return self.model.objects.filter(
            blog__author__username=self.kwargs['username'])

class NewPostView(TemplateView):
    template_name = 'blog/new.html'
