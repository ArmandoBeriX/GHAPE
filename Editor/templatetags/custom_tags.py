from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Obtiene un valor de un diccionario o devuelve lista vacía si no existe"""
    return dictionary.get(key, [])

register = template.Library()  # Esto es obligatorio

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Obtiene un valor de un diccionario usando una clave."""
    return dictionary.get(key, [])  # Retorna lista vacía si la clave no existe