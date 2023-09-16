from pprint import pprint

from django.contrib.auth.models import User
from rest_framework import (
    generics,
    permissions,
    viewsets,
    status,
)
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        if 'cliente' in request.data:
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
            except KeyError:
                errors.update({
                    'cliente': {'apelido': ["KeyError"]}
                })

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
            except KeyError:
                errors.update({
                    'bordado': {'nome': ["KeyError"]}
                })

            pedido = Pedido(cliente=cliente)
            pedido.save()

            pedido_item = PedidoItem(
                pedido=pedido,
                ordem=1,
                bordado=bordado,
            )
            pedido_item.save()

            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                PedidoItemSerializer(pedido_item).data,
                status=status.HTTP_201_CREATED,
            )

        return super().create(request, *args, **kwargs)


class PedidoBordadoClientecreate(generics.CreateAPIView):
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
