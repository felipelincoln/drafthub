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

