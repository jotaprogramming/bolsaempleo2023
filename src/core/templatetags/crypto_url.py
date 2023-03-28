from django import template
from django.core import signing

register = template.Library()

@register.filter
def encrypt_param(param):
    return signing.dumps(param)