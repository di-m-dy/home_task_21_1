from django import template

register = template.Library()


@register.simple_tag
def mymedia(data):
    if data:
        return f'/media/{data}'
    return '#'

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
