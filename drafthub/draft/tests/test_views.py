from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from drafthub.draft.views import (
    DraftCreateView, DraftDetailView, DraftUpdateView, DraftDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    LikeRedirectView,
    FavoriteRedirectView,
    TagListView,
)

from drafthub.draft.models import Draft, Tag


Blog = get_user_model()


class NewViewsTests(TestCase):
    def setUp(self):
        self.kwargs = {'username':'myblog', 'password':'pswrd'}
        self.blog = Blog.objects.create_user(**self.kwargs)
        self.url = reverse('new')

    def test_new_template(self):
        self.client.login(**self.kwargs)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'draft/form.html')

    def test_new_post(self):
        draft_kwargs = {
            'title': 'Im trying to publish this draft',
            'github_url': \
            'https://github.com/felipelincoln/drafthub/blob/master/README.md',

            'abstract': 'this is the abstract'
        }
        response = self.client.post(self.url, draft_kwargs)
        self.assertEqual(response.status_code, 302)

    def test_new_post_authenticated(self):
        self.client.login(**self.kwargs)
        draft_kwargs = {
            'title': 'Im trying to publish this draft',
            'github_url': \
            'https://github.com/felipelincoln/drafthub/blob/master/README.md',

            'abstract': 'this is the abstract'
        }
        response = self.client.post(self.url, draft_kwargs)
        self.assertTemplateUsed(response, 'draft/form.html')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

        
class TagViewsTests(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(username='myblog')
        self.tag = Tag.objects.create(name='mytag')
        self.url = reverse('tag', args=(self.tag.name,))

    def test_tag_template(self):
        self.assertTemplateUsed(self.client.get(self.url), 'draft/tag.html')

    def test_tag_context(self):
        draft1 = Draft.objects.create(blog=self.blog, slug='mydraft1')
        draft1.tags.add(self.tag)

        request = self.client.get(self.url)
        self.assertEqual(request.context['tag'], self.tag)
        self.assertEqual(request.context['tag_drafts'].count(), 1)
        self.assertIn(draft1, request.context['tag_drafts'])

    def test_tag_ordering(self):
        request = self.client.get(self.url)
        order = ('-last_activities', '-created')
        self.assertEqual(request.context['tag_drafts'].query.order_by, order)
        

class DraftViewsTests(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create_user(username='myblog', password='000')
        self.draft = Draft.objects.create(
            blog=self.blog,
            slug='my-draft',
            github_url=\
            'https://github.com/felipelincoln/drafthub/blob/master/README.md'
        )
        self.url = reverse('draft', args=('myblog', 'my-draft'))

    def test_draft_template(self):
        self.assertTemplateUsed(self.client.get(self.url), 'draft/draft.html')

    def test_draft_context(self):
        self.assertEqual(self.client.get(self.url).context['draft'],self.draft)

    def test_draft_context_authenticated(self):
        self.client.login(username='myblog', password='000')
        self.assertEqual(self.client.get(self.url).context['draft'],self.draft)
