from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from drafthub.draft.models import Blog
from drafthub.core.views import (
    HomeView, SearchListView, LoginView, BlogUpdateView, BlogListView
)


class HomeUrlsTestCase(SimpleTestCase):
    def test_home_view_class(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, HomeView)


class SearchUrlsTestCase(SimpleTestCase):
    def test_search_view_class(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func.view_class, SearchListView)


class LogoutUrlsSimpletestCase(SimpleTestCase):
    def test_logout_view_class(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)


class LoginUrlsSimpletestCase(SimpleTestCase):
    def test_login_view_class(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)


class EditUrlsSimpletestCase(SimpleTestCase):
    def test_edit_view_class(self):
        url = reverse('edit')
        self.assertEqual(resolve(url).func.view_class, BlogUpdateView)


class BlogUrlsSimpletestCase(TestCase):
    def setUp(self):
        Blog.objects.create(username='test')

    def test_blog_view_class(self):
        url = reverse('blog', args=('test',)) 
        self.assertEqual(resolve(url).func.view_class, BlogListView)

    def test_blog_not_found(self):
        url = reverse('blog', args=(' ',))
        response = self.client.get(resolve(url))
        self.assertEqual(response.status_code, 404)
