from django import template
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all()
    except Group.DoesNotExist:
        return False