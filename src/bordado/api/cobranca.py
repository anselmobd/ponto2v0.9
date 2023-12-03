from pprint import pprint

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
)
from rest_framework import (
    permissions,
    viewsets,
    status,
)
from rest_framework.response import Response

from o2lib.dict import dict_keys_value

from bordado.api.rest_consts import __ACTIONS
from bordado.models import (
    Cliente,
    Cobranca,
    PedidoItem,
    PedidoItemCobranca,
)
from bordado.serializers import CobrancaSerializer


__all__ = [
    'CobrancaViewSet',
]


@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['cobranca'])))
class CobrancaViewSet(viewsets.ModelViewSet):
    queryset = Cobranca.objects.all()
    serializer_class = CobrancaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cliente__apelido']

    def create(self, request, *args, **kwargs):
        print('CobrancaViewSet create')
        if 'pedidos_itens' in request.data:
            print('CobrancaViewSet create if')
            pprint(request.data)
            try:
                errors = {
                    'human': [],
                    'tech': [],
                }

                try:
                    print('CobrancaViewSet try cliente')
                    cliente = Cliente.objects.get(
                        apelido=request.data['cliente']['apelido']
                    )
                except KeyError as e:
                    print('CobrancaViewSet KeyError cliente')
                    errors['human'].append("Informe apelido de cliente.")
                    errors['tech'].append(repr(e))
                    raise TypeError

                try:
                    print('CobrancaViewSet cria cobranca')
                    cobranca = Cobranca(
                        cliente=cliente,
                        tipo=request.data.get('tipo'),
                        nf=request.data.get('nf'),
                        valor=request.data.get('valor'),
                        data=request.data.get('data'),
                        parcelamento=request.data.get('parcelamento'),
                        usuario=self.request.user,
                    )
                    cobranca.save()
                except Exception as e:
                    print('CobrancaViewSet cobranca.save exception')
                    errors['human'].append("Erro ao criar o registro de cobrança.")
                    errors['tech'].append(repr(e))
                    raise TypeError

                for pedido_item_id in request.data['pedidos_itens']:
                    print(pedido_item_id)
                    try:
                        print('CobrancaViewSet try pedido_item')
                        pedido_item = PedidoItem.objects.get(id=pedido_item_id)
                    except Exception as e:
                        print('CobrancaViewSet except pedido_item')
                        errors['human'].append("Erro ao buscar por pedido marcado.")
                        errors['tech'].append(repr(e))
                        raise TypeError
                    
                    try:
                        pedido_item_cobranca = PedidoItemCobranca(
                            pedido_item=pedido_item,
                            cobranca=cobranca,
                            valor=(
                                (pedido_item.quantidade * pedido_item.preco) +
                                pedido_item.programacao +
                                pedido_item.ajuste
                            )

                        )
                        pedido_item_cobranca.save()
                    except Exception as e:
                        print('CobrancaViewSet except pedido_item_cobranca')
                        errors['human'].append("Erro ao inserir registro que liga cobrança ao pedido.")
                        errors['tech'].append(repr(e))
                        raise TypeError

                return Response(
                    CobrancaSerializer(cobranca).data,
                    status=status.HTTP_201_CREATED,
                )
            except Exception:
                print('CobrancaViewSet Exception')
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)
