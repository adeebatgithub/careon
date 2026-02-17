from django import template
import math

register = template.Library()


@register.filter
def ceil(value):
    return math.ceil(value)
