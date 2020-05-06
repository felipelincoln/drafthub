from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from drafthub.core.views import (
    BlogUpdateView, BlogListView, HomeView, LoginView, SearchListView
)
from drafthub.draft.models import Draft, Tag


Blog = get_user_model()


class HomeViewTests(TestCase):
    def setUp(self): 
        self.url = reverse('home')
        self.response = self.client.get(self.url)

    def test_home_template(self):
        self.assertTemplateUsed(self.response, 'core/home.html')

    def test_home_empty_context(self):
        self.assertEqual(self.response.context['home_drafts'].count(), 0)
        self.assertEqual(self.response.context['home_tags'].count(), 0)

    def test_home_fill_context(self):
        blog = Blog.objects.create(username='testblog')
        tag = Tag.objects.create(name='test-tag')
        draft = Draft.objects.create(blog=blog, slug='draft-test')
        draft.tags.add(tag)
        response = self.client.get(self.url)

        self.assertEqual(response.context['home_drafts'].count(), 1)
        self.assertEqual(response.context['home_tags'].count(), 1)


class SearchViewTests(TestCase):
    def setUp(self):
        self.url = reverse('search')

        blog = Blog.objects.create(username='myblog')
        blog.set_password('mypassword')
        blog.save()
        tag = Tag.objects.create(name='mytag')
        draft = Draft.objects.create(
            did='myblog/lorem-ipsum-dolor-sit-amet',
            blog=blog,
            slug='lorem-ipsum-dolor-sit-amet',
            title='lorem ipsum dolor sit amet',
            abstract='this is a way to fill up content',
        )
        draft.tags.add(tag)

    def test_search_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'core/search.html')

    # ?q=[value]

    def test_search_no_q_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], None)
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], [])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], '')

    def test_search_q_empty_context(self):
        response = self.client.get(self.url, {'q':''})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], None)
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], [])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], '')

    def test_search_what_test_context(self):
        response = self.client.get(self.url, {'q':'test'})
        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], None)
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], ['test'])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], '')

    def test_search_what_lorem_context(self):
        response = self.client.get(self.url, {'q':'lorem'})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], None)
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], ['lorem'])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], '')


    # ?q=tags:[value]

    def test_search_where_tags_context(self):
        response = self.client.get(self.url, {'q':'tags:'})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], 'tags')
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], [])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], 'tags:')

    def test_search_where_tags_what_test_context(self):
        response = self.client.get(self.url, {'q':'tags:test'})
        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], 'tags')
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], ['test'])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], 'tags:')


    # ?q=blogs:[value]

    def test_search_where_blogs_context(self):
        response = self.client.get(self.url, {'q':'blogs:'})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], 'blogs')
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], [])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], 'blogs:')

    def test_search_where_blogs_what_test_context(self):
        response = self.client.get(self.url, {'q':'blogs:test'})
        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], 'blogs')
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], ['test'])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], 'blogs:')


    # ?q=favorites:[value]

    def test_search_where_favorites_context(self):
        response = self.client.get(self.url, {'q':'favorites:'})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], 'favorites')
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], [])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], 'favorites:')

    def test_search_where_favorites_what_test_context(self):
        response = self.client.get(self.url, {'q':'favorites:test'})
        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], 'favorites')
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], ['test'])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], 'favorites:')

    def test_search_where_favorites_context_authenticated(self):
        self.client.login(username='myblog', password='mypassword')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(self.url, {'q':'favorites:'})

        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], 'favorites')
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], [])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], 'favorites:')

    def test_search_where_favorites_what_test_context_authenticated(self):
        self.client.login(username='myblog', password='mypassword')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(self.url, {'q':'favorites:test'})

        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], 'favorites')
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], ['test'])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], 'favorites:')


    # ?q=tags.<name>:[value]

    def test_search_where_tags_who_test_context(self):
        response = self.client.get(self.url, {'q':'tags.test:'})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], None)
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], [])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], '')

    def test_search_where_tags_who_test_what_teste_context(self):
        response = self.client.get(self.url, {'q':'tags.test:teste'})
        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], None)
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], ['teste'])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], '')

    def test_search_where_tags_who_test_what_teste_teste2_context(self):
        response = self.client.get(self.url, {'q':'tags.test:teste teste2'})
        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], None)
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], ['teste', 'teste2'])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], '')

    def test_search_where_tags_who_mytag_context(self):
        response = self.client.get(self.url, {'q':'tags.mytag:'})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], 'tags')
        self.assertEqual(response.context['search_who'], 'mytag')
        self.assertEqual(response.context['search_what'], [])
        self.assertEqual(response.context['search_multi_who'], ['mytag'])
        self.assertEqual(response.context['search_input_value'], 'tags.mytag:')

    def test_search_where_tags_who_mytag_what_test_context(self):
        response = self.client.get(self.url, {'q':'tags.mytag:test'})
        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], 'tags')
        self.assertEqual(response.context['search_who'], 'mytag')
        self.assertEqual(response.context['search_what'], ['test'])
        self.assertEqual(response.context['search_multi_who'], ['mytag'])
        self.assertEqual(response.context['search_input_value'], 'tags.mytag:')

    def test_search_where_tags_who_mytag_what_test_teste_context(self):
        response = self.client.get(self.url, {'q':'tags.mytag:test teste'})
        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], 'tags')
        self.assertEqual(response.context['search_who'], 'mytag')
        self.assertEqual(response.context['search_what'], ['test', 'teste'])
        self.assertEqual(response.context['search_multi_who'], ['mytag'])
        self.assertEqual(response.context['search_input_value'], 'tags.mytag:')

    def test_search_match_title_where_tags_who_mytag_context(self):
        response = self.client.get(self.url, {'q':'tags.mytag:lorem TASDFE'})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], 'tags')
        self.assertEqual(response.context['search_who'], 'mytag')
        self.assertEqual(response.context['search_what'], ['lorem', 'TASDFE'])
        self.assertEqual(response.context['search_multi_who'], ['mytag'])
        self.assertEqual(response.context['search_input_value'], 'tags.mytag:')

    def test_search_match_abstract_where_tags_who_mytag_context(self):
        response = self.client.get(self.url, {'q':'tags.mytag:ISJADIUA way'})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], 'tags')
        self.assertEqual(response.context['search_who'], 'mytag')
        self.assertEqual(response.context['search_what'], ['ISJADIUA', 'way'])
        self.assertEqual(response.context['search_multi_who'], ['mytag'])
        self.assertEqual(response.context['search_input_value'], 'tags.mytag:')

    # ?q=blogs.<name>:[value]

    def test_search_where_blogs_who_test_context(self):
        response = self.client.get(self.url, {'q':'blogs.test:'})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], None)
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], [])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], '')

    def test_search_where_blogs_who_test_what_teste_context(self):
        response = self.client.get(self.url, {'q':'blogs.test:teste'})
        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], None)
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], ['teste'])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], '')

    def test_search_where_blogs_who_test_what_teste_teste2_context(self):
        response = self.client.get(self.url, {'q':'blogs.test:teste teste2'})
        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], None)
        self.assertEqual(response.context['search_who'], None)
        self.assertEqual(response.context['search_what'], ['teste', 'teste2'])
        self.assertEqual(response.context['search_multi_who'], [])
        self.assertEqual(response.context['search_input_value'], '')

    def test_search_where_blogs_who_mytag_context(self):
        response = self.client.get(self.url, {'q':'blogs.myblog:'})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], 'blogs')
        self.assertEqual(response.context['search_who'], 'myblog')
        self.assertEqual(response.context['search_what'], [])
        self.assertEqual(response.context['search_multi_who'], ['myblog'])
        self.assertEqual(
            response.context['search_input_value'],
            'blogs.myblog:'
        )

    def test_search_where_blogs_who_mytag_what_test_context(self):
        response = self.client.get(self.url, {'q':'blogs.myblog:test'})
        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], 'blogs')
        self.assertEqual(response.context['search_who'], 'myblog')
        self.assertEqual(response.context['search_what'], ['test'])
        self.assertEqual(response.context['search_multi_who'], ['myblog'])
        self.assertEqual(
            response.context['search_input_value'],
            'blogs.myblog:'
        )

    def test_search_where_blogs_who_mytag_what_test_teste_context(self):
        response = self.client.get(self.url, {'q':'blogs.myblog:test teste'})
        self.assertEqual(response.context['search_content'].count(), 0)
        self.assertEqual(response.context['search_where'], 'blogs')
        self.assertEqual(response.context['search_who'], 'myblog')
        self.assertEqual(response.context['search_what'], ['test', 'teste'])
        self.assertEqual(response.context['search_multi_who'], ['myblog'])
        self.assertEqual(
            response.context['search_input_value'],
            'blogs.myblog:'
        )

    def test_search_match_title_where_blogs_who_mytag_context(self):
        response = self.client.get(self.url, {'q':'blogs.myblog:lorem TASDFE'})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], 'blogs')
        self.assertEqual(response.context['search_who'], 'myblog')
        self.assertEqual(response.context['search_what'], ['lorem', 'TASDFE'])
        self.assertEqual(response.context['search_multi_who'], ['myblog'])
        self.assertEqual(
            response.context['search_input_value'],
            'blogs.myblog:',
        )

    def test_search_match_abstract_where_blogs_who_mytag_context(self):
        response = self.client.get(self.url, {'q':'blogs.myblog:ISJADIUA way'})
        self.assertEqual(response.context['search_content'].count(), 1)
        self.assertEqual(response.context['search_where'], 'blogs')
        self.assertEqual(response.context['search_who'], 'myblog')
        self.assertEqual(response.context['search_what'], ['ISJADIUA', 'way'])
        self.assertEqual(response.context['search_multi_who'], ['myblog'])
        self.assertEqual(
            response.context['search_input_value'],
            'blogs.myblog:',
        )

