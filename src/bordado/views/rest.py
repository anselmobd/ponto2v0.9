from pprint import pprint

from rest_framework import viewsets
from rest_framework import permissions

from bordado.models import (
    Cliente
)
from bordado.serializers import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
