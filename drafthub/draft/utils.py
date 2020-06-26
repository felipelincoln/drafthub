import random
import string
import re


CHAR_STRING = string.ascii_lowercase + string.digits

def generate_random_string(chars=CHAR_STRING, size=6):
    return ''.join(random.choice(chars) for _ in range(size))

def get_data_from_url(url):
    raw_origin = 'https://raw.githubusercontent.com'
    re_url = '^https?:\/\/github\.com\/(.+)\/(.+)\/blob\/(.+?)\/(.+)$'
    match_url = re.compile(re_url)
    match_results = match_url.match(url)

    if not match_results:
        return None

    login, repo, branch, name = match_results.groups()
    raw = '/'.join([raw_origin, *match_results.groups()])
    parent = url.rstrip(name)
    
    data = {
        'login': login,
        'repo': repo,
        'branch': branch,
        'parent': parent,
        'name': name,
        'raw': raw
    }

    return data

def shorten_string(string, max_len):
    short = string
    if len(short) > max_len:
        short = short[:max_len-3]
        short = short.rstrip()
        short = short + '...'

    return short



import requests
import re
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


def markdown(github_url):
    url = github_url
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
