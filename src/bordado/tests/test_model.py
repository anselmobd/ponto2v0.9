from django.test import TestCase

from bordado.models import Cliente


class ClienteTestCase(TestCase):
    fixtures = ["test_bordado.json"]

    def test_cadastro(self):
        """Cliente cadastrado"""
        cliente = Cliente.objects.get(apelido="Primeiro")
        # self.assertEqual(cliente.apelido, "Primeiro")
        self.assertEqual(cliente.nome, "Primeiro Confecções")
        self.assertEqual(cliente.cnpj9, 1)
        self.assertEqual(cliente.cnpj4, 1)
        self.assertEqual(cliente.cnpj2, 0)
        self.assertEqual(cliente.boleto, True)
        self.assertEqual(cliente.conta_corrente, False)
        self.assertEqual(cliente.parcela, 10)
        self.assertEqual(cliente.cnpj, "00000001/0001-00!")
