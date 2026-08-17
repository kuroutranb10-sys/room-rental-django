from django import template


register = template.Library()


@register.filter
def money(value):

    if value is None:
        return ''

    try:
        value = int(value)
    except (ValueError, TypeError):
        return value

    return f"{value:,}".replace(",", ".")