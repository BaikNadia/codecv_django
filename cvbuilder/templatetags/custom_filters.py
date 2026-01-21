from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """Умножает value на arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def get_item(dictionary, key):
    """Получает значение из словаря по ключу"""
    return dictionary.get(key)


@register.filter
def truncate_chars(value, max_length):
    """Обрезает строку до указанной длины"""
    if len(value) <= max_length:
        return value
    return value[:max_length] + "..."
