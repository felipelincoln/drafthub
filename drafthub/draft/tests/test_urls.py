from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model

from drafthub.draft.models import Draft, Tag, Comment
from drafthub.draft.views import (
    DraftCreateView, DraftDetailView, DraftUpdateView, DraftDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    LikeRedirectView,
    FavoriteRedirectView,
    TagListView,
)


Blog = get_user_model()


class NewUrlsSimpleTestCase(SimpleTestCase):
    def test_new_view_class(self):
        url = reverse('new')
        self.assertEqual(resolve(url).func.view_class, DraftCreateView)


class TagUrlsTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(name='test-tag')

    def test_tag_view_class(self):
        url = reverse('tag', args=('test-tag',))
        self.assertEqual(resolve(url).func.view_class, TagListView)

    def test_tag_not_found(self):
        url = reverse('tag', args=(' ',))
        response = self.client.get(resolve(url))
        self.assertEqual(response.status_code, 404)
        

class DraftUrlsTestCase(TestCase):
    def setUp(self):
        self.args = ('testblog', 'test-slug',)
        self.blog = Blog.objects.create(username=self.args[0])
        self.draft = Draft.objects.create(slug=self.args[1], blog=self.blog)

    def test_draft_view_class(self):
        url = reverse('draft', args=self.args)
        self.assertEqual(resolve(url).func.view_class, DraftDetailView)

    def test_draft_not_found(self):
        url = reverse('draft', args=('-', '-',))
        response = self.client.get(resolve(url))
        self.assertEqual(response.status_code, 404)

    def test_draft_edit_view_class(self):
        url = reverse('draft-edit', args=self.args)
        self.assertEqual(resolve(url).func.view_class, DraftUpdateView)
        
    def test_draft_delete_view_class(self):
        url = reverse('draft-delete', args=self.args)
        self.assertEqual(resolve(url).func.view_class, DraftDeleteView)
        
    def test_draft_like_view_class(self):
        url = reverse('draft-like', args=self.args)
        self.assertEqual(resolve(url).func.view_class, LikeRedirectView)
        
    def test_draft_favorite_view_class(self):
        url = reverse('draft-favorite', args=self.args)
        self.assertEqual(resolve(url).func.view_class, FavoriteRedirectView)


class CommentUrlsTestCase(TestCase):
    def setUp(self):
        self.args = ('testblog2', 'test-slug-2',)
        self.blog = Blog.objects.create(username=self.args[0])
        self.draft = Draft.objects.create(slug=self.args[1], blog=self.blog)
        self.comment = Comment.objects.create(blog=self.blog, draft=self.draft)
        
    def test_comment_new_view_class(self):
        url = reverse('comment-new', args=self.args)
        self.assertEqual(resolve(url).func.view_class, CommentCreateView)

    def test_comment_edit_view_class(self):
        url = reverse('comment-edit', args=(*self.args, self.comment.pk))
        self.assertEqual(resolve(url).func.view_class, CommentUpdateView)

    def test_comment_edit_not_found(self):
        url = reverse('comment-edit', args=(*self.args, self.comment.pk+1))
        response = self.client.get(resolve(url))
        self.assertEqual(response.status_code, 404)

    def test_comment_delete_view_class(self):
        url = reverse('comment-delete', args=(*self.args, self.comment.pk))
        self.assertEqual(resolve(url).func.view_class, CommentDeleteView)

    def test_comment_delete_not_found(self):
        url = reverse('comment-delete', args=(*self.args, self.comment.pk+1))
        response = self.client.get(resolve(url))
        self.assertEqual(response.status_code, 404)
