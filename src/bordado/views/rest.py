from pprint import pprint

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

from bordado.models import *
from bordado.serializers import *


__all__ = [
    'UserViewSet',
    'ClienteViewSet',
]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
