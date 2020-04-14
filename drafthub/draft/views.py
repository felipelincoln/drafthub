from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import get_user_model


from .models import Draft
from .forms import DraftForm


Blog = get_user_model()


class BlogListView(ListView):
    paginate_by = 5
    model = Draft

    def get_queryset(self):
        return self.model.objects.filter(
            blog__username=self.kwargs['username'])


class DraftDetailView(DetailView):
    model = Draft

    def get_queryset(self):
        return self.model.objects.filter(
            blog__username=self.kwargs['username'])


class DraftCreateView(LoginRequiredMixin, CreateView):
    form_class = DraftForm
    template_name = 'draft/draft_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request

        return kwargs

    def form_valid(self, form):
        form.instance.blog = self.request.user
        form.instance.slug = self.get_draft_unique_slug(form.instance)

        return super().form_valid(form)

    def get_draft_unique_slug(self, instance, unique_len=6):
        from django.utils.text import slugify
        from .utils import generate_random_string

        max_length = Draft._meta.get_field('slug').max_length
        author = instance.blog.username
        non_unique_slug = slugify(instance.title)
        non_unique_slug = non_unique_slug[: max_length - unique_len - 1]

        if non_unique_slug.endswith('-'):
            non_unique_slug = non_unique_slug[:-1]

        slug = non_unique_slug
        while Draft.objects.filter(slug=slug, blog__username=author):
            unique = generate_random_string()
            slug = non_unique_slug + '-' + unique

        return slug


class DraftUpdateView(LoginRequiredMixin, UpdateView):
    form_class = DraftForm
    template_name = 'draft/draft_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request

        return kwargs

    def get_queryset(self):
        return Draft.objects.filter(
            blog__username=self.kwargs['username'])

    def user_has_access(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return request.user == self.object.blog
        return redirect_to_login(request.get_full_path())

    def dispatch(self, request, *args, **kwargs):
        if not self.user_has_access(request):
            return redirect(self.object)
        return super().dispatch(request, *args, **kwargs)


class DraftDeleteView(LoginRequiredMixin, DeleteView):
    model = Draft

    def get_queryset(self):
        return self.model.objects.filter(
            blog__username=self.kwargs['username'])

    def user_has_access(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return request.user == self.object.blog
        return redirect_to_login(request.get_full_path())

    def dispatch(self, request, *args, **kwargs):
        if not self.user_has_access(request):
            return redirect(self.object)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        args = (self.kwargs['username'],)
        return reverse_lazy('blog', args=args)
