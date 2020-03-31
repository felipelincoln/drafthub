from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect


class HomeView(TemplateView):
    template_name = 'core/home.html'


def logout_view(request):
    logout(request)
    return redirect('home')
