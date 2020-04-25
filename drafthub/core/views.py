from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.views.generic import ListView
from drafthub.draft.models import Draft, Tag
from django.db.models import Q, Count
import re

Blog = get_user_model()


class HomeView(ListView):
    paginate_by = 5
    model = Draft
    context_object_name = 'home_drafts'
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.annotate(num_drafts=Count('tagged_drafts'))
        context.update({
            'tags': tags.order_by('-num_drafts')[:15],
        })

        return context


class LoginView(auth_views.LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True


class SearchEngine:
    # search pattern where.who: what
    where = ''
    who = ''
    what = []
    content = Draft.objects

    def __init__(self, request):
        self.request = request
        q = request.GET.get('q')
        template = '^(?:(favorites|blogs|tags)(?:\.(\w+))?:)?\s*(.*?)\s*$'
        re_object = re.compile(template)
        self.where, self.who, self.what = re_object.match(q).groups()
        self.what = self.what.split()

        self._set_content_from_where()
        self._filter_content_from_who()
        self._filter_content_from_what()

    def _set_content_from_where(self):
        if not self.who:
            content = self.content
            if self.where == 'blogs':
                content = Blog.objects
            elif self.where == 'tags':
                content = Tag.objects
            elif self.where == 'favorites':
                content = self.request.user.favorited_drafts 
            self.content = content

    def _filter_content_from_who(self):
        if self.who: #implies where is valid
            if self.where in ['favorites', 'blogs']:
                blogs = Blog.objects.filter(username__icontains=self.who)
                if blogs.exists():
                    if self.where == 'favorites':
                        querysets = [x.favorited_drafts.all() for x in blogs]
                    elif self.where == 'blogs':
                        querysets = [x.my_drafts.all() for x in blogs]

                    content = querysets.pop()
                    for queryset in querysets:
                        content |= queryset
                else:
                    content = self._filter_not_found()
            elif self.where == 'tags':
                drafts = Draft.objects.filter(tags__name__icontains=self.who)
                if drafts.exists():
                    content = drafts
                else:
                    content = self._filter_not_found()
            self.content = content

    def _filter_content_from_what(self):
        content = self.content
        if self.what:
            if self.where in ['tags', 'blogs'] and not self.who:
                if self.where == 'blogs':
                    querysets = [
                        content.filter(username__icontains=x) for x in self.what
                    ]
                elif self.where == 'tags':
                    querysets = [
                        content.filter(name__icontains=x) for x in self.what
                    ]
            else:
                querysets = (
                    [content.filter(title__icontains=x) for x in self.what]
                    + [content.filter(abstract__icontains=x) for x in self.what]
                )

                if not self.where and not self.who:
                    querysets += [
                        content.filter(blog__username__icontains=x) for x in self.what
                    ]
            content = querysets.pop()
            for queryset in querysets:
                content |= queryset
        self.content = content


    def _filter_not_found(self):
        self.who = None
        self.where = None
        return self.content


class SearchListView(ListView):
    context_object_name = 'search_content'
    template_name = 'core/search.html'

    def get_queryset(self):
        a = SearchEngine(self.request)
        return a.content.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_content'] = context['search_content'][:25]
        return context
