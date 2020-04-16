from django.contrib.auth import views as auth_views
from django.views.generic import ListView
from drafthub.draft.models import Draft
from django.db.models import Q

class HomeView(ListView):
    paginate_by = 5
    model = Draft
    context_object_name = 'blog_content'
    template_name = 'core/home.html'


class LoginView(auth_views.LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True


class SearchListView(ListView):
    paginate_by = 5
    model = Draft
    context_object_name = 'search_content'
    template_name = 'core/search.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            q_split = q.split()

            title_queries = [Q(title__icontains=value) for value in q_split]
            abstract_queries = [Q(abstract__icontains=value) for value in q_split]
            blog_queries = [Q(blog__username__icontains=value) for value in q_split]

            queries = title_queries + abstract_queries + blog_queries
            query = queries.pop()

            for item in queries:
                query |= item

            return self.model.objects.filter(query)

        else:
            return self.model.objects.all()
