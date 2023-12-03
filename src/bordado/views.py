from pprint import pprint

from django.shortcuts import redirect, render


__all__ = ['index', 'sobre']


def index(request):
    if request.user.is_authenticated:
        return render(request, 'bordado/index/main.html', {})
    else:
        return redirect('bordado:sobre')



def sobre(request):
    return render(request, 'bordado/sobre.html', {})
