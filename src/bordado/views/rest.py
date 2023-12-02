from pprint import pprint

from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    generics,
    permissions,
    viewsets,
    status,
)
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
)
from bordado.models import *
from bordado.serializers import *
from o2lib.dict import dict_keys_value

from bordado.views.pedido_item import PedidoItemViewSet
from bordado.views.rest_consts import *


__all__ = [
    'UserViewSet',
    'ClienteViewSet',
    'DificuldadeBordadoViewSet',
    'BordadoViewSet',
    'PedidoViewSet',
    'PedidoItemViewSet',
    'CobrancaViewSet',
    'PedidoItemCobrancaViewSet',
    'OrdemProducaoViewSet',
    'ApontamentoProducaoViewSet',
]


@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['user'])))
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['cliente'])))
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
        

@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['dificuldade_bordado'])))
class DificuldadeBordadoViewSet(viewsets.ModelViewSet):
    queryset = DificuldadeBordado.objects.all()
    serializer_class = DificuldadeBordadoSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['bordado'])))
class BordadoViewSet(viewsets.ModelViewSet):
    queryset = Bordado.objects.all()
    serializer_class = BordadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['cliente__apelido']


@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['pedido'])))
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['cobranca'])))
class CobrancaViewSet(viewsets.ModelViewSet):
    queryset = Cobranca.objects.all()
    serializer_class = CobrancaSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['pedido_item_cobranca'])))
class PedidoItemCobrancaViewSet(viewsets.ModelViewSet):
    queryset = PedidoItemCobranca.objects.all()
    serializer_class = PedidoItemCobrancaSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['pedido_bordado'])))
class PedidoBordadoClientecreate(generics.CreateAPIView):
    queryset = PedidoItem.objects.all().order_by('-inserido_em')
    serializer_class = PedidoItemSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['apontamento_producao'])))
class ApontamentoProducaoViewSet(viewsets.ModelViewSet):
    queryset = ApontamentoProducao.objects.all()
    serializer_class = ApontamentoProducaoSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['ordem_producao'])))
class OrdemProducaoViewSet(viewsets.ModelViewSet):
    queryset = OrdemProducao.objects.all()
    serializer_class = OrdemProducaoSerializer
    permission_classes = [permissions.IsAuthenticated]
