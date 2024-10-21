from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})

@register.filter(name='replace_underscore')
def replace_underscore(value):
    return value.replace('_', ' ')
