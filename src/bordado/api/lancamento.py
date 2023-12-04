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
    Lancamento,
)
from bordado.serializers import LancamentoSerializer


__all__ = [
    'LancamentoViewSet',
]


@extend_schema_view(
    **dict_keys_value(__ACTIONS, extend_schema(tags=['lancamento'])))
class LancamentoViewSet(viewsets.ModelViewSet):
    queryset = Lancamento.objects.all()
    serializer_class = LancamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cliente__apelido']

    def create(self, request, *args, **kwargs):
        print('LancamentoViewSet create')
        if len(request.data.keys()) == 4:
            print('LancamentoViewSet create if')
            pprint(request.data)
            # ['cliente', 'data', 'informacao', 'valor']:
            try:
                errors = {
                    'human': [],
                    'tech': [],
                }

                try:
                    print('LancamentoViewSet try cliente')
                    cliente = Cliente.objects.get(
                        apelido=request.data['cliente']['apelido']
                    )
                except KeyError as e:
                    print('LancamentoViewSet KeyError cliente')
                    errors['human'].append("Informe apelido de cliente.")
                    errors['tech'].append(repr(e))
                    raise TypeError

                try:
                    print('LancamentoViewSet cria lancamento')
                    lancamento = Lancamento(
                        cliente=cliente,
                        data=request.data.get('data'),
                        informacao=request.data.get('informacao'),
                        valor=request.data.get('valor'),
                        usuario=self.request.user,
                    )
                    lancamento.save()
                except Exception as e:
                    print('LancamentoViewSet cobranca.save exception')
                    errors['human'].append("Erro ao criar o registro de lancamento.")
                    errors['tech'].append(repr(e))
                    raise TypeError

                return Response(
                    LancamentoSerializer(lancamento).data,
                    status=status.HTTP_201_CREATED,
                )
            except Exception:
                print('LancamentoViewSet Exception')
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)
