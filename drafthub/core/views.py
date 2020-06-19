import re
from django.db.models import Value, Case, When, IntegerField
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, TemplateView
from django.shortcuts import get_object_or_404

from drafthub.draft.models import Draft, Tag


Blog = get_user_model()


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['bio', 'email', 'text']
    template_name = 'draft/form.html'
    context_object_name = 'blog'

    def get_object(self):
        obj = get_object_or_404(Blog, username=self.request.user)
        return obj

class BlogListView(ListView):
    model = Draft
    template_name = 'draft/blog.html'
    context_object_name = 'blog_drafts'
    paginate_by = 20

    def get_queryset(self):
        self.blog = get_object_or_404(Blog, username=self.kwargs['blog'])
        return self.model.objects.filter(blog=self.blog).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.blog.social_auth.exists():
            context['github'] = self.blog.social_auth.get().extra_data
        context.update({
            'blog': self.blog,
            })

        return context


class HomeView(ListView):
    model = Draft
    context_object_name = 'drafts_new'
    template_name = 'core/home.html'
    paginate_by = 3

    def get_queryset(self):
        return Draft.objects.all().order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'home_tags': Tag.objects.all(),
            'home_blogs': Blog.objects.all(),
            'drafts_pop': Draft.objects.all(),
        })

        return context


class LoginView(auth_views.LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True


class SearchEngine:
    # search pattern where.who: what
    MAX_RESULTS = 30
    where = None
    who = None
    what = []
    content = Draft.objects

    multi_who = []

    def __init__(self, request):
        self.request = request
        if 'q' in request.GET.keys():
            q = request.GET.get('q')
            template = '^(?:(favorites|blogs|tags)(?:\.(\w+))?:)?\s*(.*?)\s*$'
            re_object = re.compile(template)
            self.where, self.who, self.what = re_object.match(q).groups()
            self.what = self.what.split()

            self._set_content_from_where()
            self._filter_content_from_who()
            self._filter_content_from_what()


    @property
    def results(self):
        content = {'search_content': self.content.all()[:self.MAX_RESULTS]}

        if not self.where:
            q = self.request.GET.get('q')
            self.request.GET._mutable = True
            self.request.GET.__setitem__('q', f'tags:{q}')

            tag_search = SearchEngine(self.request)
            tag_results = tag_search.results['search_content']
            content.update({'search_content_tags': tag_results})

            self.request.GET.__setitem__('q', f'blogs:{q}')
            blog_search = SearchEngine(self.request)
            blog_results = blog_search.results['search_content']
            content.update({'search_content_blogs': blog_results})
            self.request.GET._mutable = False

        return content

    @property
    def metadata(self):
        input_value = ''
        if self.where:
            input_value += self.where
        if self.who:
            input_value += '.' + self.who
        if input_value:
            input_value += ':'

        meta = {
            'search_where': self.where,
            'search_who': self.who,
            'search_what': self.what,
            'search_multi_who': self.multi_who,
            'search_input_value': input_value
        }
        return meta


    def _set_content_from_where(self):
        if not self.who:
            content = self.content
            if self.where == 'blogs':
                content = Blog.objects
            elif self.where == 'tags':
                content = Tag.objects
            elif self.where == 'favorites':
                if self.request.user.is_authenticated:
                    content = self.request.user.favorited_drafts 
            self.content = content

    def _filter_content_from_who(self):
        if self.who: #implies where is valid
            if self.where in ['favorites', 'blogs']:
                blogs = Blog.objects.filter(username__icontains=self.who)
                if blogs.exists():
                    self.multi_who = [blog.username for blog in blogs]
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
                    self.multi_who = [
                        tag.name for tag in Tag.objects.filter(
                            name__icontains=self.who
                        )
                    ]
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
                        content.filter(
                            username__icontains=x
                        ) for x in self.what
                    ]
                elif self.where == 'tags':
                    querysets = [
                        content.filter(name__icontains=x) for x in self.what
                    ]
            else:
                querysets = (
                    [content.filter(title__icontains=x) for x in self.what]
                    +[content.filter(abstract__icontains=x) for x in self.what]
                )

                if not self.where and not self.who:
                    querysets += [
                        content.filter(
                            blog__username__icontains=x
                        ) for x in self.what
                    ] + [
                        content.filter(
                            tags__name__icontains=x
                        ) for x in self.what
                    ]

            score = {}
            for queryset in querysets:
                for instance in queryset:
                    k = instance.pk
                    score[k] = score.setdefault(k, 0) + 1

            content = content.filter(pk__in=score).annotate(
                score=Case(
                    *[When(pk=k, then=Value(v)) for k,v in score.items()],
                    output_field=IntegerField()
                ),
            )
            content = content.order_by('-score', *content.query.order_by)
        self.content = content


    def _filter_not_found(self):
        self.who = None
        self.where = None
        return self.content


class SearchListView(TemplateView):
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = SearchEngine(self.request)
        context.update({
             **search.results,
             **search.metadata
        })
        return context
