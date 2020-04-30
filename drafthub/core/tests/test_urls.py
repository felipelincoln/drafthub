from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from drafthub.core.views import HomeView, LoginView, SearchListView


class HomeUrlsTestCase(TestCase):
    def test_home_view_class(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_home_url_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_home_reverse_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    

class SearchUrlsTestCase(TestCase):
    def test_search_view_class(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func.view_class, SearchListView)

    def test_search_url_status_code(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)
    
    def test_search_reverse_status_code(self):
        url = reverse('search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class LogoutUrlsSimpletestCase(SimpleTestCase):
    def test_logout_view_class(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)

    def test_logout_url_status_code(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
    
    def test_logout_reverse_status_code(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class LoginUrlsSimpletestCase(SimpleTestCase):
    def test_login_view_class(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_login_url_status_code(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_reverse_status_code(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
