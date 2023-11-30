from django.contrib.auth.models import User
from rest_framework import serializers

from bordado.models import *


__all__ = [
    'UserSerializer',
    'ClienteSerializer',
    'DificuldadeBordadoSerializer',
    'BordadoSerializer',
    'SetBordadoSerializer',
    'PedidoSerializer',
    'PedidoItemSerializer',
    'OrdemProducaoSerializer',
    'ApontamentoProducaoSerializer',
]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]
        read_only=True


class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    # usuario = UserSerializer()
    class Meta:
        model = Cliente
        fields = [
            'id',
            'nome',
            'apelido',
            'cnpj9',
            'cnpj4',
            'cnpj2',
            'boleto',
            'conta_corrente',
            'parcela',
            # 'usuario',
            'quando',
        ]


class DificuldadeBordadoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DificuldadeBordado
        fields = [
            'id',
            'ordem',
            'descricao',
        ]


class BordadoSerializer(serializers.HyperlinkedModelSerializer):
    cliente = ClienteSerializer()
    dificuldade = DificuldadeBordadoSerializer()
    class Meta:
        model = Bordado
        fields = [
            'id',
            'cliente',
            'nome',
            'pontos',
            'cores',
            'tamanho_maximo',
            'dificuldade',
        ]


class SetBordadoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bordado
        fields = [
            'id',
            'nome',
            'pontos',
            'cores',
            'tamanho_maximo',
        ]


class PedidoSerializer(serializers.HyperlinkedModelSerializer):
    cliente = ClienteSerializer()
    class Meta:
        model = Pedido
        fields = [
            'numero',
            'cliente',
            'inserido_em',
            'entrega',
            'cancelado',
        ]


class PedidoItemSerializer(serializers.HyperlinkedModelSerializer):
    pedido = PedidoSerializer()
    bordado = BordadoSerializer()
    usuario = UserSerializer()

    class Meta:
        model = PedidoItem
        fields = [
            'id',
            'pedido',
            'ordem',
            'inserido_em',
            'bordado',
            'quantidade',
            'preco',
            'cancelado',
            'usuario',
        ]


class OrdemProducaoSerializer(serializers.HyperlinkedModelSerializer):
    pedido_item = PedidoItemSerializer()
    class Meta:
        model = OrdemProducao
        fields = [
            'numero',
            'pedido_item',
            'quantidade',
            'cancelado',
            'inserido_em',
        ]


class ApontamentoProducaoSerializer(serializers.HyperlinkedModelSerializer):
    op = OrdemProducaoSerializer()
    class Meta:
        model = ApontamentoProducao
        fields = [
            'op',
            'qtd_perda',
            'qtd_prod',
            'apontado_em',
            'encerrado',
        ]
