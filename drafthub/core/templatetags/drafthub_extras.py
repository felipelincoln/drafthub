import requests
import re
from django import template
from django.utils.safestring import mark_safe
import markdown as _markdown
import bleach
from pymdownx import emoji

from drafthub.draft.utils import get_data_from_url


markdown_kwargs = {
    'extensions':[
        'pymdownx.superfences',
        'markdown.extensions.tables',
        'pymdownx.betterem',
        'pymdownx.tilde',
        'pymdownx.emoji',
        'pymdownx.tasklist',
        'pymdownx.magiclink',
        'pymdownx.arithmatex',
    ],
    'extension_configs':{
        'pymdownx.tilde': {
            'subscript': False
        },
        'pymdownx.emoji':{
            'emoji_index': emoji.gemoji,
            'emoji_generator': emoji.to_png,
            'alt': 'short',
            'options': {
                'attributes': {
                    'align': 'absmiddle',
                    'height': '20px',
                    'width': '20px'
                },
            }
        },
        'pymdownx.arithmatex':{
            'generic': True,
        }
    }
}
bleach_kwargs = {
    'tags': [
	'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
	'b', 'i', 'strong', 'em', 'tt', 'del',
	'p', 'br',
	'span', 'div', 'blockquote', 'code', 'hr', 'pre',
	'ul', 'ol', 'li', 'dd', 'dt', 'dl',
	'img',
	'a',
	'sub', 'sup',
        'table', 'thead','td', 'tr', 'th', 'tbody',
        'input', # allow only type, checked and disabled
    ],
    'attributes':{
        '*': lambda *_: 1,
    }
}


register = template.Library()

@register.filter
@mark_safe
def markdown(instance):
    url = instance.github_url
    data = get_data_from_url(url)

    raw = data['raw']
    login = data['login']
    repo = data['repo']
    parent = data['parent']

    markdown_kwargs['extension_configs']['pymdownx.magiclink'] = {
        'repo_url_shortener': True,
        'repo_url_shorthand': True,
        'social_url_shorthand': True,
        'provider': 'github',
        'user': login,
        'repo': repo,
    }

    url_response = requests.get(raw)
    unsafe_content = url_response.text

    re_links = '\[(.*)\]\((?!https?:\/\/|#)(.+)\)'
    match_links = re.compile(re_links)
    content_transform = match_links.sub(
        r'[\1](' + parent + r'\2)', unsafe_content)

    markdown_content = _markdown.markdown(content_transform, **markdown_kwargs)
    sanitized_content = bleach.clean(markdown_content, **bleach_kwargs)

    return sanitized_content

@register.filter
@mark_safe
def plaintext_markdown(text):
    markdown_content = _markdown.markdown(text, **markdown_kwargs)
    sanitized_content = bleach.clean(markdown_content, **bleach_kwargs)

    return sanitized_content


@register.filter
def count_range(n):
    return range(1,n+1)

@register.filter
def in_queryset(blog, queryset):
    return blog in queryset

@register.filter
def get_model_name(queryset):
    return queryset[0]._meta.model_name

@register.filter
def timesince_format(value):
    return value.split(',')[0]
