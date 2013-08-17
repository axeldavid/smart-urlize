from django import template
from django.utils.html import mark_safe

from ..smarturlize import SmartUrlize

register = template.Library()


@register.filter
def smart_urlize(text, transformers=''):

    include = []
    exclude = []

    if transformers and transformers.startswith('-'):
        exclude = transformers.strip('-').split(',')
    elif transformers:
        include = transformers.split(',')

    urlizer = SmartUrlize()
    return mark_safe(urlizer(text, include=include, exclude=exclude))
