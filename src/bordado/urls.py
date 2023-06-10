from django.urls import path

from .views import *


app_name = 'bordado'
urlpatterns = [
    path('', index, name='index'),
    path('sobre', sobre, name='sobre'),
]
