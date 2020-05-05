from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Draft, Tag, Comment, Activity
from .forms import DraftForm


Blog = get_user_model()


class QueryFromBlog:
    def get_queryset(self):
        return Draft.objects.filter(
            blog__username=self.kwargs['blog'])
 

class AccessRequired:
    def _user_has_access(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return request.user == self.object.blog
        return redirect_to_login(request.get_full_path())

    def dispatch(self, request, *args, **kwargs):
        if not self._user_has_access(request):
            return redirect(self.object)
        return super().dispatch(request, *args, **kwargs)


class DraftCreateView(LoginRequiredMixin, CreateView):
    form_class = DraftForm
    template_name = 'draft/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_type': 'draft_create',
        })

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request

        return kwargs

    def form_valid(self, form):
        form.instance.blog = self.request.user
        form.instance.slug = self._get_slug(form.instance)
        form.instance.did = self._get_did(form.instance)
        form.save()
        self._set_tags(form)

        return super().form_valid(form)

    def _get_slug(self, instance, unique_len=6):
        from django.utils.text import slugify
        from .utils import generate_random_string

        max_length = Draft._meta.get_field('slug').max_length
        author = instance.blog.username
        non_unique_slug = slugify(instance.title)
        non_unique_slug = non_unique_slug[: max_length - unique_len - 1]

        if non_unique_slug.endswith('-'):
            non_unique_slug = non_unique_slug[:-1]

        slug = non_unique_slug
        while Draft.objects.filter(did=instance.get_did(author,slug)).exists():
            unique = generate_random_string()
            slug = non_unique_slug + '-' + unique

        return slug

    def _set_tags(self, form):
        tags = form.cleaned_data['tags']
        draft = form.instance

        if tags:
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                draft.tags.add(tag)

    def _get_did(self, instance):
        blog = instance.blog
        slug = instance.slug
        return instance.get_did(blog, slug)


class DraftDetailView(QueryFromBlog, DetailView):
    model = Draft
    template_name = 'draft/draft.html'
    context_object_name = 'draft'

    def get_object(self):
        obj = super().get_object()
        referer = self.request.META.get('HTTP_REFERER') or ''

        if not self.request.user in obj.views:
            if not obj.get_absolute_url() in referer:
                obj.hits += 1
                obj.save(update_fields=['hits'])

        if self.request.user.is_authenticated:
            activity, created = Activity.objects.get_or_create(
                blog=self.request.user,
                draft=obj
            )
            if not created:
                activity.save(update_fields=['viewed'])

            if self.request.user.social_auth.exists():
                obj.last_update = self._get_updated(obj)
                if obj.last_update:
                    obj.save(update_fields=['updated'])

        return obj

    def _get_updated(self, obj):
        import requests
        import json
        from django.utils.dateparse import parse_datetime
        from .utils import get_data_from_url

        user = self.request.user
        social_user = self.request.user.social_auth.get()
        extra_data = social_user.extra_data
        token = extra_data['access_token']
        data = get_data_from_url(obj.github_url) 

        endpoint = 'https://api.github.com/graphql'
        query = f"""query {{
  viewer {{
    login
  }}
  rateLimit {{
    limit
    cost
    remaining
  }}
  repository(owner: "{data['login']}", name: "{data['repo']}"){{
    object(expression: "{data['branch']}"){{
      ... on Commit {{
        history(path: "{data['name']}", first:1){{
          edges {{
            node {{
              message
              oid
              author {{
                date
                user {{
                  name
                  url
                  login
                  isViewer
                }}
              }}
            }}
          }}
        }}
      }}
    }}
  }}
}}"""

        headers = {'Authorization': f'bearer {token}'}
        GraphiQL_connect = requests.post(
            endpoint,
            json={'query': query},
            headers=headers
        )
        api_data = json.loads(GraphiQL_connect.text)

        last_commit = api_data['data']['repository']['object']['history']
        last_commit = last_commit['edges'][0]['node']['author']['date']
        last_commit = parse_datetime(last_commit)

        tzinfo = last_commit.tzinfo
        last_commit = last_commit.replace(tzinfo=tzinfo).astimezone(tz=None)

        if last_commit > obj.created:
            return last_commit

        return None


class DraftUpdateView(QueryFromBlog, AccessRequired, LoginRequiredMixin,
                      UpdateView):

    form_class = DraftForm
    template_name = 'draft/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_type': 'draft_edit',
        })

        return context

    def form_valid(self, form):
        form.instance.tags.clear()
        self._set_tags(form)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request

        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        tags = self.object.tags.all().values_list('name', flat=True)
        initial.update({
            'tags': ', '.join(tags),
        })

        return initial


    def _set_tags(self, form):
        tags = form.cleaned_data['tags']
        draft = form.instance

        if tags:
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                draft.tags.add(tag)


class DraftDeleteView(QueryFromBlog, AccessRequired, LoginRequiredMixin,
                      DeleteView):

    model = Draft
    template_name = 'draft/form.html'
    context_object_name = 'draft'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_type': 'draft_delete',
        })

        return context

    def get_success_url(self):
        args = (self.kwargs['blog'],)
        return reverse_lazy('blog', args=args)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'draft/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_type': 'comment_create',
            'comment_draft': get_object_or_404(
                Draft,
                slug=self.kwargs['slug'],
                blog__username=self.kwargs['blog']
            )
        })
        
        return context

    def get_initial(self):
        initial = super().get_initial()
        if 'quote' in self.request.GET.keys():

            quote_comment_pk = self.request.GET['quote']
            comment = Comment.objects.filter(pk=quote_comment_pk)
            if not comment.exists():
                return initial

            comment = comment.get()
            quoted_content = '\n> '.join(comment.content.splitlines())
            initial['content'] = \
                '> **[{} said:](#{})**  \n> {}\n\n'.format(
                comment.blog.username,
                comment.pk,
                quoted_content,
            )
        return initial

    def form_valid(self, form):
        form.instance.blog = self.request.user
        form.instance.draft = get_object_or_404(
            Draft,
            slug=self.kwargs['slug'],
            blog__username=self.kwargs['blog']
        )
        form.save()

        return super().form_valid(form)


class CommentUpdateView(AccessRequired, LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'draft/form.html'
    fields = ['content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_type': 'comment_edit',
            'comment_draft':get_object_or_404(
                Draft,
                slug=self.kwargs['slug'],
                blog__username=self.kwargs['blog']
            )
        })
        
        return context

    def form_valid(self, form):
        form.instance.updated = timezone.now()
        form.save()

        return super().form_valid(form)


class CommentDeleteView(AccessRequired, LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'draft/form.html'
    context_object_name = 'comment'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_type': 'comment_delete',
            'comment_draft':get_object_or_404(
                Draft,
                slug=self.kwargs['slug'],
                blog__username=self.kwargs['blog']
            )
        })
        
        return context

    def get_success_url(self):
        kwargs = {
            'blog': self.kwargs['blog'],
            'slug': self.kwargs['slug'],
        }
        return reverse_lazy('draft', kwargs=kwargs)+"#third-content"


class LikeRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        blog = self.kwargs.get('blog')
        obj = get_object_or_404(Draft, slug=slug, blog__username=blog)

        activity = Activity.objects.filter(blog=self.request.user, draft=obj)
        if activity.exists():
            activity = activity.get()
            if activity.liked:
                activity.liked = None
            else:
                activity.liked = timezone.now()

            activity.save(update_fields=['liked'])
        else:
            activity = Activity(blog=self.request.user, draft=obj)
            activity.liked = timezone.now()
            activity.save()

        return obj.get_absolute_url()


class FavoriteRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        blog = self.kwargs.get('blog')
        obj = get_object_or_404(Draft, slug=slug, blog__username=blog)

        activity = Activity.objects.filter(blog=self.request.user, draft=obj)
        if activity.exists():
            activity = activity.get()
            if activity.favorited:
                activity.favorited = None
            else:
                activity.favorited = timezone.now()

            activity.save(update_fields=['favorited'])
        else:
            activity = Activity(blog=self.request.user, draft=obj)
            activity.favorited = timezone.now()
            activity.save()

        return obj.get_absolute_url()


class TagListView(ListView):
    model = Draft
    template_name = 'draft/tag.html'
    context_object_name = 'tag_drafts'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, name=self.kwargs['tag'])
        return self.model.objects.filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'tag': self.tag,
        })

        return context
