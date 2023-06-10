from pprint import pprint

from django.shortcuts import render


__all__ = ['index', 'sobre']


def index(request):
    return render(request, 'bordado/index.html', {})


def sobre(request):
    return render(request, 'bordado/sobre.html', {})
