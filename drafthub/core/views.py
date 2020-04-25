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


class SearchEngine:     # where.who: what
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

    def _filter_content_from_what(self): # BUGGY
        content = self.content
        if not self.where and not self.who:
            print('filter by blog__username')

        elif not self.who and self.where != 'favorites':
            if self.where == 'blogs':
                querysets = [
                    content.filter(username__icontains=x) for x in self.what
                ]
            elif self.where == 'tags':
                querysets = [
                    content.filter(name__icontains=x) for x in self.what
                ]
            content = querysets.pop()
            for queryset in querysets:
                content |= queryset
            return

        print('filter by abstract and title')
                






        self.content = content


    def _filter_not_found(self):
        self.who = None
        self.where = None
        return self.content




class SearchListView(ListView):
    context_object_name = 'search_content'
    template_name = 'core/search.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        q_startswith = ('favorites:', 'tags:', 'blogs:')
        q_favorites, q_tags, q_blogs = [q.startswith(x) for x in q_startswith]
        self.q_clean = ''
        self.q_filter = ''

        a = SearchEngine(self.request)
        print(a.content.all())

        if q_blogs:
            self.q_clean = q.lstrip('blogs:').strip()
            self.q_filter = 'blogs'
            return Blog.objects.filter(username__icontains=self.q_clean)

        elif q_tags:
            self.q_clean = q.lstrip('tags:').strip()
            self.q_filter = 'tags'
            return Tag.objects.filter(name__icontains=self.q_clean)

        elif q:
            content_source = Draft.objects
            self.q_clean = q.strip()
            if q_favorites:
                self.q_clean = q.lstrip('favorites:').strip()
                self.q_filter = 'favorites'
                content_source = self.request.user.favorited_drafts
                if not self.q_clean:
                    return content_source.all()
#            else:
#                if ':' in self.q_clean:
#                    q_custom = self.q_clean.partition(':')          # where.who: what
#                    q_custom_what = q_custom[2]
#                    q_custom_how = q_custom[0].partition('.')[0]
#                    q_custom_where = q_custom[0].partition('.')[2]
#
#                    if q_custom[0].startswith('tag.'):
#                    
#                    elif q_custom[0].startswith('blog.'):
#
#                    custom = Tag.objects.filter(name__icontains=q_custom[0])
#                    if custom.exists():
#                        self.q_clean = q_custom[2].strip()
#                        self.q_filter = ' '.join([tag.name for tag in custom])
#                        content_source = Draft.objects
#                        for tag in custom:
#                            content_source = content_source.filter(tags__name__icontains=tag.name)
#
#                        print(content_source.all())
#                        if not self.q_clean:
#                            return content_source.all()


            q_clean_list = self.q_clean.split()

            title_queries = [Q(title__icontains=value) for value in q_clean_list]
            abstract_queries = [Q(abstract__icontains=value) for value in q_clean_list]
            blog_queries = [Q(blog__username__icontains=value) for value in q_clean_list]

            queries = title_queries + abstract_queries + blog_queries
            query = queries.pop()

            for x in queries:
                query |= x

            return content_source.filter(query)

        else:
            return Draft.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_query': self.q_clean,
            'search_filter': self.q_filter
        })
        context['search_content'] = context['search_content'][:25]
        return context
