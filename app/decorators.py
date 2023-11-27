from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def group_required(group_name, redirect_url='ruta_a_tu_pagina_de_error'):
    def in_group(user):
        if not user.is_authenticated:
            return False
        try:
            group = Group.objects.get(name=group_name)
            return group in user.groups.all()
        except Group.DoesNotExist:
            return False

    def decorator(view_func):
        @user_passes_test(in_group)
        def _wrapped_view(request, *args, **kwargs):
            if not in_group(request.user):
                group_error = f"No tienes permisos para acceder a esta página."
                return render(request, redirect_url, {'group_error': group_error})
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator
