import re
import requests
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
import markdown as pymd


register = template.Library()

@register.filter
@mark_safe
def markdown(instance):
    url_origin = instance.github_url.rsplit('/', 1)[0] + '/'
    url_noblob = instance.github_url.replace('blob/', '')
    url_stripped = url_noblob.lstrip('https://github.com/')
    url_raw = 'https://raw.githubusercontent.com/' + url_stripped

    content = requests.get(url_raw)
    content = content.text
    
    re_links = '\[(.*)\]\((?!https?:\/\/)(.+)\)'
    match_links = re.compile(re_links)
    content_transform = match_links.sub(
        r'[\1](' + url_origin + r'\2)', content)

    content_esc = escape(content_transform)
    return pymd.markdown(content_esc)


@register.filter
def n_range(n):
    return range(n)
