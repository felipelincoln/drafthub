import requests
from django import template
from django.template.defaultfilters import stringfilter
import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(url):
    content = requests.get(url)
    content = content.text
    return md.markdown(content, extensions=['markdown.extensions.fenced_code'])

@register.filter()
def n_range(n):
    return range(n)
