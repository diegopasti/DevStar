from django import template

register = template.Library()

@register.filter
def comman_to_dot(string):
    return string.replace(",",".")