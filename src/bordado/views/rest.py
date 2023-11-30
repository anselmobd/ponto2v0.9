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


__ACTIONS = ('create', 'retrieve', 'update', 'partial_update', 'destroy', 'list')


@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['user'])))
class UserViewSet(viewsets.ModelViewSet):
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
    **dict_keys_value(__ACTIONS, extend_schema(tags=['pedido_item'])))
class PedidoItemViewSet(viewsets.ModelViewSet):
    queryset = PedidoItem.objects.all().order_by('-inserido_em')
    serializer_class = PedidoItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pedido__cliente__apelido']

    def destroy(self, request, *args, **kwargs):
        """Alé de apagar o PedidoItem indicado, apaga também o pedido,
        o bordado e o cliente, desde que estes não sejam utilizados por 
        nenhum outro registro.
        """
        pedido_item = PedidoItem.objects.get(
            id=kwargs['pk']
        )

        result = super().destroy(request, *args, **kwargs)

        if pedido_item:
            pedido_numero = pedido_item.pedido.numero
            bordado_id = pedido_item.bordado.id
            cliente_id = pedido_item.bordado.cliente.id
            try:
                Pedido.objects.get(numero=pedido_numero).delete()
            except ProtectedError:
                pass
            try:
                Bordado.objects.get(id=bordado_id).delete()
            except ProtectedError:
                pass
            try:
                Cliente.objects.get(id=cliente_id).delete()
            except ProtectedError:
                pass

        return result

    def create(self, request, *args, **kwargs):
        if 'cliente' in request.data:
            try:
                errors = {}
                try:
                    cliente = Cliente.objects.get(
                        apelido=request.data['cliente']['apelido']
                    )
                except Cliente.DoesNotExist:
                    serializer = ClienteSerializer(data=request.data['cliente'])
                    if serializer.is_valid():
                        cliente = serializer.save(usuario=self.request.user)
                    else:
                        errors.update(serializer.errors)
                        raise TypeError
                except KeyError:
                    errors.update({
                        'cliente': {'apelido': ["KeyError"]}
                    })
                    raise TypeError

                try:
                    bordado = Bordado.objects.get(
                        cliente=cliente,
                        nome=request.data['bordado']['nome'],
                    )
                except Bordado.DoesNotExist:
                    serializer = SetBordadoSerializer(data=request.data['bordado'])
                    if serializer.is_valid():
                        bordado = serializer.save(cliente=cliente)
                    else:
                        errors.update(serializer.errors)
                        raise TypeError
                except KeyError:
                    errors.update({
                        'bordado': {'nome': ["KeyError"]}
                    })
                    raise TypeError

                pedido = Pedido(cliente=cliente)
                pedido.save()

                pedido_item = PedidoItem(
                    pedido=pedido,
                    ordem=1,
                    bordado=bordado,
                )
                pedido_item.save()

                return Response(
                    PedidoItemSerializer(pedido_item).data,
                    status=status.HTTP_201_CREATED,
                )
            except Exception:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


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
