from django import template

register = template.Library()


@register.filter()
def get_number(items):
    """
    Нумерация строк в таблице
    """
    return items.pop(0)