from django.views.generic import TemplateView, ListView
from django.contrib.auth import logout
from django.shortcuts import redirect
from drafthub.apps.post.models import Post

class HomeView(ListView):
    model = Post
    template_name = 'core/home.html'


def logout_view(request):
    logout(request)
    return redirect('home')
