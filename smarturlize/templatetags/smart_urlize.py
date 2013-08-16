from django import template
from django.utils.html import mark_safe

from smarturlize import SmartUrlize

register = template.Library()


@register.filter
def smart_urlize(text):
    urlizer = SmartUrlize()
    return mark_safe(urlizer(text))
