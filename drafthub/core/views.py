from django.contrib.auth import views as auth_views
from django.views.generic import ListView
from drafthub.draft.models import Draft

class HomeView(ListView):
    paginate_by = 5
    model = Draft
    template_name = 'core/home.html'

class LoginView(auth_views.LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
