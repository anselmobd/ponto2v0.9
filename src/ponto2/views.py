from pprint import pprint

from django.shortcuts import redirect


__all__ = ['index']


def index(request):
    return redirect('bordado:index')
