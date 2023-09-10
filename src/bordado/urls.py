from django.urls import include, path
from rest_framework import routers

from .views.views import *
from .views.rest import ClienteViewSet


router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet)

app_name = 'bordado'
urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name='index'),
    path('sobre', sobre, name='sobre'),
]
