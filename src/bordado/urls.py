from django.urls import path

from .views.views import *


app_name = 'bordado'
urlpatterns = [
    path('index', index, name='index'),
    path('sobre', sobre, name='sobre'),
]
