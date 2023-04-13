from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from o2lib.codes.cnpj import CNPJ


__all__ = [
    'Cliente',
    'DificuldadeBordado',
    'Bordado',
    'OrdemProducao',
]


# class Empresa(models.Model):
#     nome = models.CharField(
#         max_length=50,
#         unique=True,
#     )

#     def __str__(self):
#         return f'{self.nome}'

#     class Meta:
#         db_table = "po2_empresa"
#         verbose_name = "Empresa"
#         ordering = ['nome']


class Cliente(models.Model):
    # empresa = models.ForeignKey(
    #     Empresa,
    #     on_delete=models.PROTECT,
    # )
    nome = models.CharField(
        max_length=50,
    )
    cnpj9 = models.PositiveIntegerField(
        'CNPJ (raiz)',
        validators=[MinValueValidator(1), MaxValueValidator(999_999_999)],
    )
    cnpj4 = models.PositiveSmallIntegerField(
        'CNPJ (filial)',
        validators=[MinValueValidator(1), MaxValueValidator(9_999)],
    )
    cnpj2 = models.PositiveSmallIntegerField(
        'CNPJ (dígitos)',
        validators=[MinValueValidator(0), MaxValueValidator(99)],
    )
    boleto = models.BooleanField(
        'Gera boleto?',
        default=False,
    )
    conta_corrente = models.BooleanField(
        'Trabalha como conta corrente?',
        default=False,
    )
    parcela = models.PositiveSmallIntegerField(
        'Número de parcelas padrão',
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=1,
    )

    @property
    def cnpj(self):
        cnpj = CNPJ(self.cnpj9, self.cnpj4, self.cnpj2)
        mark = "" if cnpj.valid() else "!"
        return f"{cnpj}{mark}"

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        db_table = "po2_cliente"
        verbose_name = "Cliente"
        ordering = ['nome']
        unique_together = [['cnpj9', 'cnpj4', 'cnpj2']]


class DificuldadeBordado(models.Model):
    ordem = models.PositiveSmallIntegerField(
        unique=True,
    )
    descricao = models.CharField(
        'Descrição',
        max_length=50,
        unique=True,
    )

    def id_indefinida():
        return DificuldadeBordado.objects.get(ordem=0).id

    def __str__(self):
        return f'{self.descricao}'

    class Meta:
        db_table = "po2_dificuldade_bordado"
        verbose_name = "Dificuldade de bordado"
        verbose_name_plural = "Dificuldades de bordado"
        ordering = ['ordem']


class Bordado(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
    )
    nome = models.CharField(
        max_length=50,
    )
    pontos = models.PositiveIntegerField(
        default=0,
    )
    cores = models.PositiveIntegerField(
        default=0,
    )
    tamanho_maximo = models.PositiveIntegerField(
        'tamanho máximo',
        default=0,
        help_text="em milímetros",
    )
    dificuldade = models.ForeignKey(
        DificuldadeBordado,
        on_delete=models.PROTECT,
        default=DificuldadeBordado.id_indefinida,
    )

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        db_table = "po2_bordado"
        verbose_name = "Bordado"
        ordering = ['nome']
        unique_together = [['cliente', 'nome']]


class OrdemProducao(models.Model):
    numero = models.AutoField(
        'Número',
        primary_key=True
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    bordado = models.ForeignKey(
        Bordado,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1_000_000)],
        default=0,
    )
    cancelado = models.BooleanField(
        default=False,
    )
    inserido_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OP {self.numero} / {self.cliente.nome} / {self.bordado.nome}"

    class Meta:
        db_table = "po2_op"
        verbose_name = "Ordem de produção"
        verbose_name_plural = "Ordens de produção"
        ordering = ['-numero']


# class ApontamentoProducao(models.Model):

#     op = models.ForeignKey(
#         OrdemProducao,
#         on_delete=models.PROTECT,
#         blank=False,
#         null=False,
#     )
#     qtd_perda = models.IntegerField(
#         'quantidade de perda',
#         validators=[MinValueValidator(1), MaxValueValidator(1_000_000)],
#         default=0,
#     )
#     qtd_prod = models.IntegerField(
#         'quantidade produzida',
#         validators=[MinValueValidator(1), MaxValueValidator(1_000_000)],
#         default=0,
#     )
#     apontado_em = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"OP {self.numero} "

#     class Meta:
#         db_table = "po2_aponta_prod"
#         verbose_name = "Apontamento de produção"
#         verbose_name_plural = "Apontamentos de produção"
#         ordering = ['-op_id', 'apontado_em']
