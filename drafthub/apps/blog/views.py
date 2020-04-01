from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from drafthub.apps.post.models import Post
from .forms import NewPostForm

class BlogView(ListView):
    paginate_by = 5
    model = Post
    template_name = 'blog/blog.html'

    def get_queryset(self):
        return self.model.objects.filter(
            blog__author__username=self.kwargs['username'])


def new_post_view(request):
    form = NewPostForm(request.POST or None)
    context = {'form': form}

    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.blog = request.user.blog
        new_post.save()

        form = NewPostForm()
        context = {'form': form}

    if request.user.is_authenticated:
        return render(request, 'blog/new.html', context)
    else:
        raise Http404
