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
    regex_expr = '^https:\/\/github\.com\/(.+?)\/(.+?)\/blob\/(.*\.md)$'
    regex_tester = re.compile(regex_expr)
    regex_results = regex_tester.match(instance.github_url)

    handle, repo, md = regex_results.groups()
    raw_github_url = f'https://raw.githubusercontent.com/{handle}/{repo}/{md}'

    content = requests.get(raw_github_url)
    content = content.text
    content = escape(content)
    return pymd.markdown(content)


@register.filter
def n_range(n):
    return range(n)
