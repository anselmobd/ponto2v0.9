from pprint import pprint

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

from bordado.models import *
from bordado.serializers import *


__all__ = [
    'UserViewSet',
    'ClienteViewSet',
    'DificuldadeBordadoViewSet',
    'BordadoViewSet',
    'PedidoViewSet',
    'PedidoItemViewSet',
    'OrdemProducaoViewSet',
    'ApontamentoProducaoViewSet',
]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
        

class DificuldadeBordadoViewSet(viewsets.ModelViewSet):
    queryset = DificuldadeBordado.objects.all()
    serializer_class = DificuldadeBordadoSerializer
    permission_classes = [permissions.IsAuthenticated]


class BordadoViewSet(viewsets.ModelViewSet):
    queryset = Bordado.objects.all()
    serializer_class = BordadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['cliente__apelido']


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]


class PedidoItemViewSet(viewsets.ModelViewSet):
    queryset = PedidoItem.objects.all().order_by('-inserido_em')
    serializer_class = PedidoItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApontamentoProducaoViewSet(viewsets.ModelViewSet):
    queryset = ApontamentoProducao.objects.all()
    serializer_class = ApontamentoProducaoSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrdemProducaoViewSet(viewsets.ModelViewSet):
    queryset = OrdemProducao.objects.all()
    serializer_class = OrdemProducaoSerializer
    permission_classes = [permissions.IsAuthenticated]
