from django.views.generic import ListView
from django.contrib.auth import logout
from django.shortcuts import redirect
from drafthub.draft.models import Draft

class HomeView(ListView):
    paginate_by = 5
    model = Draft
    template_name = 'core/home_list.html'


def logout_view(request):
    logout(request)
    return redirect('home')
