from django.contrib.auth.models import User
from rest_framework import serializers

from bordado.models import (
    Cliente
)


__all__ = [
    'UserSerializer',
    'ClienteSerializer',
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
