from django.test import TestCase
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


class NewUrlsTestCase(TestCase):
    def test_new_view_class(self):
        url = reverse('new')
        self.assertEqual(resolve(url).func.view_class, DraftCreateView)

    def test_new_status_code(self):
        url = reverse('new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_new_status_code_authenticated(self):
        args = ('test', 'testpassword')
        blog = Blog.objects.create(username=args[0])
        blog.set_password(args[1])
        blog.save()

        self.client.login(username=args[0], password=args[1])
        self.assertIn('_auth_user_id', self.client.session)

        url = reverse('new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TagUrlsTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(name='test-tag')

    def test_tag_view_class(self):
        url = reverse('tag', args=('test-tag',))
        self.assertEqual(resolve(url).func.view_class, TagListView)

    def test_tag_not_found(self):
        url = reverse('tag', args=(' ',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_tag_not_found_authenticated(self):
        args = ('test', 'testpassword')
        blog = Blog.objects.create(username=args[0])
        blog.set_password(args[1])
        blog.save()

        self.client.login(username=args[0], password=args[1])
        self.assertIn('_auth_user_id', self.client.session)

        url = reverse('tag', args=(' ',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_tag_status_code(self):
        url = reverse('tag', args=('test-tag',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_tag_status_code_authenticated(self):
        args = ('test', 'testpassword')
        blog = Blog.objects.create(username=args[0])
        blog.set_password(args[1])
        blog.save()

        self.client.login(username=args[0], password=args[1])
        self.assertIn('_auth_user_id', self.client.session)

        url = reverse('tag', args=('test-tag',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        

class DraftUrlsTestCase(TestCase):
    def setUp(self):
        self.args = ('testblog', 'test-slug',)
        self.password = 'test123'
        self.github_url = \
            'https://github.com/felipelincoln/drafthub/blob/master/README.md'
        self.blog = Blog.objects.create(username=self.args[0])
        self.blog.set_password(self.password)
        self.blog.save()
        self.draft = Draft.objects.create(
            slug=self.args[1],
            blog=self.blog,
            github_url=self.github_url
        )

    def test_draft_view_class(self):
        url = reverse('draft', args=self.args)
        self.assertEqual(resolve(url).func.view_class, DraftDetailView)

    def test_draft_not_found(self):
        url = reverse('draft', args=('-', '-',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_draft_not_found_authenticated(self):
        args = ('test', 'testpassword')
        blog = Blog.objects.create(username=args[0])
        blog.set_password(args[1])
        blog.save()

        self.client.login(username=args[0], password=args[1])
        self.assertIn('_auth_user_id', self.client.session)

        url = reverse('draft', args=('-', '-',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_draft_status_code(self):
        url = reverse('draft', args=self.args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_draft_status_code_authenticated(self):
        self.client.login(username=self.args[0], password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        url = reverse('draft', args=self.args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_draft_status_code_authenticated2(self):
        args = ('test', 'testpassword')
        blog = Blog.objects.create(username=args[0])
        blog.set_password(args[1])
        blog.save()

        self.client.login(username=args[0], password=args[1])
        self.assertIn('_auth_user_id', self.client.session)

        url = reverse('draft', args=self.args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class DrafEdittUrlsTestCase(TestCase):
    def setUp(self):
        self.args = ('testblog', 'test-slug',)
        self.password = 'test123'
        self.github_url = \
            'https://github.com/felipelincoln/drafthub/blob/master/README.md'
        self.blog = Blog.objects.create(username=self.args[0])
        self.blog.set_password(self.password)
        self.blog.save()
        self.draft = Draft.objects.create(
            slug=self.args[1],
            blog=self.blog,
            github_url=self.github_url
        )

    def test_draft_edit_view_class(self):
        url = reverse('draft-edit', args=self.args)
        self.assertEqual(resolve(url).func.view_class, DraftUpdateView)

    def test_draft_edit_not_found(self):
        url = reverse('draft-edit', args=('-', '-',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_draft_edit_not_found_authenticated(self):
        args = ('test', 'testpassword')
        blog = Blog.objects.create(username=args[0])
        blog.set_password(args[1])
        blog.save()

        self.client.login(username=args[0], password=args[1])
        self.assertIn('_auth_user_id', self.client.session)

        url = reverse('draft-edit', args=('-', '-',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_draft_edit_status_code(self):
        url = reverse('draft-edit', args=self.args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_draft_edit_status_code_authenticated(self):
        self.client.login(username=self.args[0], password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        url = reverse('draft', args=self.args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_draft_edit_status_code_authenticated2(self):
        args = ('test', 'testpassword')
        blog = Blog.objects.create(username=args[0])
        blog.set_password(args[1])
        blog.save()

        self.client.login(username=args[0], password=args[1])
        self.assertIn('_auth_user_id', self.client.session)

        url = reverse('draft-edit', args=self.args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)












class DraftEditTestCase(TestCase):
    def setUp(self):
        self.args = ('testblog', 'test-slug',)
        self.github_url = \
            'https://github.com/felipelincoln/drafthub/blob/master/README.md'
        self.blog = Blog.objects.create(username=self.args[0])
        self.draft = Draft.objects.create(
            slug=self.args[1],
            blog=self.blog,
            github_url=self.github_url
        )

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
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_comment_delete_view_class(self):
        url = reverse('comment-delete', args=(*self.args, self.comment.pk))
        self.assertEqual(resolve(url).func.view_class, CommentDeleteView)

    def test_comment_delete_not_found(self):
        url = reverse('comment-delete', args=(*self.args, self.comment.pk+1))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
