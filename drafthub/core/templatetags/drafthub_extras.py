import requests
import re
from django import template
from django.utils.safestring import mark_safe
import markdown as _markdown
import bleach
from pymdownx import emoji

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
    url_origin = url.rsplit('/', 1)[0] + '/'
    url_noblob = url.replace('blob/', '')
    url_stripped = url_noblob.lstrip('https://github.com/')
    url_raw = 'https://raw.githubusercontent.com/' + url_stripped

    re_url = '^https?:\/\/github\.com\/(.+)\/(.+)\/blob\/.*$'
    match_url = re.compile(re_url)
    match_results = match_url.match(url)
    handle, repo = match_results.groups()

    url_response = requests.get(url_raw)
    unsafe_content = url_response.text

    re_links = '\[(.*)\]\((?!https?:\/\/|#)(.+)\)'
    match_links = re.compile(re_links)
    content_transform = match_links.sub(
        r'[\1](' + url_origin + r'\2)', unsafe_content)

    markdown_kwargs['extension_configs']['pymdownx.magiclink'] = {
        'repo_url_shortener': True,
        'repo_url_shorthand': True,
        'social_url_shorthand': True,
        'provider': 'github',
        'user': handle,
        'repo': repo,
    }

    markdown_content = _markdown.markdown(content_transform, **markdown_kwargs)
    sanitized_content = bleach.clean(markdown_content, **bleach_kwargs)

    return sanitized_content


@register.filter
def n_range(n):
    return range(n)
