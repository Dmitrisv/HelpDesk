from django import template
import re

register = template.Library()


@register.filter
def linkify(value):
    url_regex = re.compile(r"(https?://[^\s]+)")
    return re.sub(url_regex, r'<a href="\1" target="_blank" >\1</a>', value)
