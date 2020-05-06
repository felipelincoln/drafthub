import time

from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.utils import timezone

from drafthub.core.views import (
    BlogUpdateView, BlogListView, HomeView, LoginView, SearchListView
)
from drafthub.draft.models import Draft, Tag, Activity


Blog = get_user_model()


class HomeViewsTests(TestCase):
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

    def test_home_drafts_ordering(self):
        # (-last_activities, -created)
        blog = Blog.objects.create(username='myblog')
        draft1 = Draft.objects.create(
            did='myblog/first-draft',
            blog=blog,
            slug='first-draft',
            title='First draft',
            abstract='this is my first draft',
        )
        time.sleep(0.1)
        draft2 = Draft.objects.create(
            did='myblog/second-draft',
            blog=blog,
            slug='second-draft',
            title='Second draft',
            abstract='this is my second draft',
        )

        def get_first():
            return self.client.get(self.url).context['home_drafts'].first()

        # draft1 created then draft2 created
        # ordering: draft2(0), draft1(0)
        self.assertEqual(get_first(), draft2)

        # myblog views draft1
        # ordering: draft1(1), draft2(0)
        activity1 = Activity.objects.create(blog=blog, draft=draft1)
        self.assertEqual(get_first(), draft1)

        # myblog view and like draft2
        # ordering: draft2(2), draft1(1)
        activity2 = Activity.objects.create(blog=blog, draft=draft2)
        activity2.liked = timezone.now()
        activity2.save()
        self.assertEqual(get_first(), draft2)

        # myblog like and favorite draft1
        # ordering: draft1(3), draft2(2)
        activity1.liked = timezone.now()
        activity1.favorited = timezone.now()
        activity1.save()
        self.assertEqual(get_first(), draft1)
        
        # myblog favorite draft2
        # ordering: draft2(3), draft1(3)
        activity2.liked = timezone.now()
        activity2.favorited = timezone.now()
        activity2.save()
        self.assertEqual(get_first(), draft2)


    def test_home_tags_ordering(self):
        # (-tagged_drafts_last_activities, last_drafts)
        blog = Blog.objects.create(username='myblog')
        tag1 = Tag.objects.create(name='first')
        tagb = Tag.objects.create(name='both')
        draft1 = Draft.objects.create(
            did='myblog/first-draft',
            blog=blog,
            slug='first-draft',
            title='First draft',
            abstract='this is my first draft',
        )
        time.sleep(0.1)
        draft2 = Draft.objects.create(
            did='myblog/second-draft',
            blog=blog,
            slug='second-draft',
            title='Second draft',
            abstract='this is my second draft',
        )
        draft1.tags.add(tag1, tagb)
        draft2.tags.add(tagb)

        def get_first():
            return self.client.get(self.url).context['home_tags'].first()

        # draft1 created then draft2 created
        # ordering: tag1(0), tagb(0)
        self.assertEqual(get_first(), tag1)

        # myblog views draft1
        # ordering: tag1(1), tagb(1)
        activity1 = Activity.objects.create(blog=blog, draft=draft1)
        self.assertEqual(get_first(), tag1)

        # myblog view and like draft2
        # ordering: tagb(3), tag1(1)
        activity2 = Activity.objects.create(blog=blog, draft=draft2)
        activity2.liked = timezone.now()
        activity2.save()
        self.assertEqual(get_first(), tagb)

        # myblog like and favorite draft1
        # ordering: tagb(5), tag1(3)
        activity1.liked = timezone.now()
        activity1.favorited = timezone.now()
        activity1.save()
        self.assertEqual(get_first(), tagb)
        
        # myblog favorite draft2
        # ordering: tagb(6), tag1(3)
        activity2.liked = timezone.now()
        activity2.favorited = timezone.now()
        activity2.save()
        self.assertEqual(get_first(), tagb)


class SearchViewsTests(TestCase):
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

class EditViewsTests(TestCase):
    def test_edit_post(self):
        blog = Blog.objects.create_user(username='myblog', password='mypass')
        self.client.login(username='myblog', password='mypass')
        self.assertIn('_auth_user_id', self.client.session)

        self.assertEqual(blog.bio, Blog._meta.get_field('bio').default)
        self.assertEqual(blog.email, '')
        self.assertEqual(blog.text, Blog._meta.get_field('text').default)

        response = self.client.post(reverse('edit'), {
            'bio': 'this is my new bio',
            'email': 'myblog@drafthub.com',
            'text': 'this text will appear in my blog page'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response._headers['location'][1],
            blog.get_absolute_url()
        )

        blog = Blog.objects.first()
        self.assertEqual(blog.bio, 'this is my new bio')
        self.assertEqual(blog.email, 'myblog@drafthub.com')
        self.assertEqual(blog.text, 'this text will appear in my blog page')


class BlogViewsTest(TestCase):
    def test_blog_drafts_ordering(self):
        # (-created,)
        url = reverse('blog', args=('myblog',))
        blog = Blog.objects.create(username='myblog')

        def get_first():
            return self.client.get(url).context['blog_drafts'].first()

        draft1 = Draft.objects.create(blog=blog, slug='1', did='myblog/1')
        self.assertEqual(get_first(), draft1)
        time.sleep(0.1)

        draft2 = Draft.objects.create(blog=blog, slug='2', did='myblog/2')
        self.assertEqual(get_first(), draft2)
        time.sleep(0.1)

        draft3 = Draft.objects.create(blog=blog, slug='3', did='myblog/3')
        self.assertEqual(get_first(), draft3)
