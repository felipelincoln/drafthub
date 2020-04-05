import requests
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe 
import markdown as md

register = template.Library()


@register.filter
@mark_safe
def markdown(instance):
    raw_start = r'https://raw.githubusercontent.com/'
    raw_end = instance.github_url.lstrip('/')

    # getting rid of /blob/
    _ = raw_end.split('/')
    del _[1]
    raw_end = '/'.join(['', *_])

    url = raw_start + instance.blog.author.username + raw_end

    print(url)
    content = requests.get(url)
    content = content.text
    content = escape(content)
    return md.markdown(content, extensions=['markdown.extensions.codehilite'])


@register.filter
def n_range(n):
    return range(n)
