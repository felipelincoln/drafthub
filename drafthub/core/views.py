from django.views.generic import ListView
from django.contrib.auth import logout
from django.shortcuts import redirect
from drafthub.blog.models import Post

class HomeView(ListView):
    paginate_by = 5
    model = Post
    template_name = 'core/home_list.html'


def logout_view(request):
    logout(request)
    return redirect('home')
