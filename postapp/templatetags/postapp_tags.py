from atexit import register
from unicodedata import category
from django import template

from postapp.models import Category


register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('postapp/categories_list.html')
def show_categories():
    categories = Category.objects.all()
    return {'categories': categories}