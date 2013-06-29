from django import template
from django.template.defaultfilters import stringfilter

from smarturlize import SmartUrlize

register = template.Library()

@register.filter
def smart_urlize(text):
    urlizer = SmartUrlize()
    return urlizer(text)
