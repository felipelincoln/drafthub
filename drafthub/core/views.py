import re
from django.db.models import Value, Case, When, IntegerField
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, TemplateView
from django.shortcuts import get_object_or_404

from drafthub.draft.models import Draft, Tag
from drafthub.utils import PageContext


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


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        def skip_n(queryset, n):
            dids = queryset.values_list('did', flat=True)[n:]
            return Draft.objects.filter(did__in=dids)

        context = super().get_context_data(**kwargs)

        n_tags = 7
        n_popular = 25
        n_latest = 10
        n_updated = 5

        tags = Tag.objects.all()
        drafts = Draft.objects.all()
        drafts_latest = skip_n(drafts, n_popular).order_by('-created')
        drafts_updated = skip_n(drafts_latest, n_latest).filter(
            updated__isnull=False
        ).order_by('-updated')
        popular_tags_by_name = [tag.name for tag in tags[:n_tags]]

        page_meta = PageContext(self.request)
        page_meta.keywords = ', '.join(popular_tags_by_name)

        context.update({
            'tags_popular': tags[:n_tags],
            'drafts_popular': drafts[:n_popular],
            'drafts_latest': drafts_latest[:n_latest],
            #'drafts_random': Draft.objects.get_random_queryset(3),
            'drafts_updated': drafts_updated[:n_updated],
             **page_meta.context,
        })

        return context


class LoginView(auth_views.LoginView):
    template_name = 'error.html'
    redirect_authenticated_user = True
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_meta = PageContext(self.request)
        page_meta.title = 'drafthub: login required'
        page_meta.error.status = (
            'To performe this action you must be logged in'
        )
        page_meta.error.verbose = ''
        page_meta.error.message = 'Is it a bug?'
        context.update({
             **page_meta.context,
        })

        return context


class SearchEngine:
    # search pattern where.who: what
    MAX_RESULTS = 30
    where = None
    who = None
    what = []
    content = Draft.objects

    multi_who = []

    def __init__(self, request, q, where=None, who=None):
        self.request = request
        self.q = q
        self.who = who
        self.where = where
        self.what = q.split() if q else []

        self._set_content_from_where()
        self._filter_content_from_who()
        self._filter_content_from_what()

    @property
    def results(self):
        content = {'search_content': self.content.all()[:self.MAX_RESULTS]}

        if not self.where:
            tag_search = SearchEngine(self.request, self.q, where='tags')
            tag_results = tag_search.results['search_content']
            content.update({'search_content_tags': tag_results})

            blog_search = SearchEngine(self.request, self.q, where='blogs')
            blog_results = blog_search.results['search_content']
            content.update({'search_content_blogs': blog_results})

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
                    +[content.filter(
                        description__icontains=x
                    ) for x in self.what]
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
        else:
            content = Draft.objects.none()
        self.content = content


    def _filter_not_found(self):
        self.who = None
        self.where = None
        return self.content


class SearchListView(TemplateView):
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get('q')
        where = self.request.GET.get('where')
        who = self.request.GET.get('who')
        search = SearchEngine(self.request, q, where, who)

        page_meta = PageContext(self.request)
        page_meta.title = 'search results for: ' + ' '.join(search.what)

        context.update({
             **search.results,
             **search.metadata,
             **page_meta.context
        })
        return context
