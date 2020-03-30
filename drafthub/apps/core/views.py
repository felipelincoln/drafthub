from django.views.generic import TemplateView
from django.contrib.auth import logout # provisional
from django.shortcuts import redirect # provisional

class HomeView(TemplateView):
    template_name = 'core/home.html'


def logout_view(request): # provisional
    logout(request)
    return redirect('home')
