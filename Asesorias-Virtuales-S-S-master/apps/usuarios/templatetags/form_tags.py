from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Agrega una clase CSS a un campo de formulario
    """
    return field.as_widget(attrs={'class': css_class})

@register.filter(name='add_placeholder')
def add_placeholder(field, placeholder):
    """
    Agrega un placeholder a un campo de formulario
    """
    return field.as_widget(attrs={'placeholder': placeholder}) 