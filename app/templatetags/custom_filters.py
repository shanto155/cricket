# custom_filters.py
from django import template

register = template.Library()


@register.filter
def over(value):
    return int(value / 6)


@register.filter
def ball(value):
    return value % 6


@register.filter
def subtract(value, arg):
    return abs(value - arg)
