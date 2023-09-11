from django.contrib.auth.models import User
from rest_framework import serializers

from bordado.models import *


__all__ = [
    'UserSerializer',
    'ClienteSerializer',
    'DificuldadeBordadoSerializer',
    'BordadoSerializer',
]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="bordado:user-detail")
    class Meta:
        model = User
        fields = [
            'url',
            'username',
            'email',
        ]


class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    usuario = UserSerializer()
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
            'usuario',
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
    dificuldade = DificuldadeBordadoSerializer()
    class Meta:
        model = Bordado
        fields = [
            'id',
            # 'cliente',
            'nome',
            'pontos',
            'cores',
            'tamanho_maximo',
            'dificuldade',
        ]
