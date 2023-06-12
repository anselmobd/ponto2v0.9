from django.test import TestCase

from bordado.models import Cliente


def cria_cliente():
    Cliente.objects.create(
        nome='teste',
        apelido='t',
        cnpj9=123456789,
        cnpj4=1234,
        cnpj2=12,
        boleto=False,
        conta_corrente=False,
        parcela=3,
    )

class ClienteTestCase(TestCase):
    def setUp(self):
        cria_cliente()

    def test_clientes(self):
        """Cliente cadastrado"""
        teste = Cliente.objects.get(apelido="t")
        self.assertEqual(teste.cnpj, "123456789/1234-12!")
