import requests
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe 
import markdown as md

register = template.Library()


@register.filter
@mark_safe
def markdown(instance):
    url = instance.github_url
    content = requests.get(url)
    content = content.text
    content = escape(content)
    return md.markdown(content, extensions=['markdown.extensions.codehilite'])


@register.filter
def n_range(n):
    return range(n)
