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
    'CobrancaSerializer',
    'PedidoItemCobrancaSerializer',
    'LancamentoSerializer',
    'OrdemProducaoSerializer',
    'ApontamentoProducaoSerializer',
]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]
        read_only=True


class ClienteSerializer(serializers.ModelSerializer):
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


class DificuldadeBordadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DificuldadeBordado
        fields = [
            'id',
            'ordem',
            'descricao',
        ]


class BordadoSerializer(serializers.ModelSerializer):
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


class SetBordadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bordado
        fields = [
            'id',
            'nome',
            'pontos',
            'cores',
            'tamanho_maximo',
        ]


class PedidoSerializer(serializers.ModelSerializer):
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


class CobrancaSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    usuario = UserSerializer()

    class Meta:
        model = Cobranca
        fields = [
            'id',
            'cliente',
            'tipo',
            'nf',
            'valor',
            'data',
            'parcelamento',
            'usuario',
            'quando',
        ]


class PedidoItemCobrancasSerializer(serializers.ModelSerializer):
    cobranca = CobrancaSerializer()

    class Meta:
        model = PedidoItemCobranca
        fields = [
            'id',
            'cobranca',
            'valor',
        ]

class LancamentoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    cobranca = CobrancaSerializer()
    usuario = UserSerializer()

    class Meta:
        model = Lancamento
        fields = [
            'id',
            'cliente',
            'data',
            'cobranca',
            'informacao',
            'valor',
            'calculando',
            'saldo_cliente',
            'saldo_empresa',
            'usuario',
            'quando',
        ]


class PedidoItemSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer()
    bordado = BordadoSerializer()
    usuario = UserSerializer()
    cobrancas = PedidoItemCobrancasSerializer(many=True, read_only=True)

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
            'programacao',
            'ajuste',
            'cobrancas',
            'cancelado',
            'usuario',
        ]


class PedidoItemCobrancaSerializer(serializers.ModelSerializer):
    pedido_item = PedidoItemSerializer()
    cobranca = CobrancaSerializer()

    class Meta:
        model = PedidoItemCobranca
        fields = [
            'id',
            'pedido_item',
            'cobranca',
            'valor',
        ]


class OrdemProducaoSerializer(serializers.ModelSerializer):
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


class ApontamentoProducaoSerializer(serializers.ModelSerializer):
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
