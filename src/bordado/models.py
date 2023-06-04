from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from o2lib.codes.cnpj import CNPJ


__all__ = [
    'Cliente',
    'DificuldadeBordado',
    'Bordado',
    'Pedido',
    'PedidoItem',
    'OrdemProducao',
    'ApontamentoProducao',
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
    admin_order = 100
    # empresa = models.ForeignKey(
    #     Empresa,
    #     on_delete=models.PROTECT,
    # )
    nome = models.CharField(
        max_length=100,
    )
    apelido = models.CharField(
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
    admin_order = 200
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
        return f'{self.ordem}-{self.descricao}'

    class Meta:
        db_table = "po2_dificuldade_bordado"
        verbose_name = "Dificuldade de bordado"
        verbose_name_plural = "Dificuldades de bordado"
        ordering = ['ordem']


class Bordado(models.Model):
    admin_order = 300
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


class Pedido(models.Model):
    admin_order = 400
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
    inserido_em = models.DateTimeField(auto_now_add=True)
    entrega = models.DateField(
        blank=True,
        null=True,
    )
    cancelado = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"Pedido {self.numero} / {self.cliente.nome}"

    class Meta:
        db_table = "po2_pedido"
        ordering = ['-numero']


class PedidoItem(models.Model):
    admin_order = 500
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    ordem = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        default=0,
    )
    inserido_em = models.DateTimeField(auto_now_add=True)
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
    preco = models.DecimalField(
        'Preço',
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(1_000_000)],
        default=0,
    )
    cancelado = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"Pedido {self.pedido.numero} (ordem {self.ordem}) {self.bordado} * {self.quantidade}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.ordem = (
                PedidoItem.objects.filter(pedido=self.pedido).count() + 1
            ) * 10
        super(PedidoItem, self).save(*args, **kwargs)

    class Meta:
        db_table = "po2_pedido_item"
        verbose_name = "Item de pedido"
        verbose_name_plural = "Itens de pedido"
        ordering = ['-pedido__numero', '-ordem']


class OrdemProducao(models.Model):
    admin_order = 600
    numero = models.AutoField(
        'Número',
        primary_key=True
    )
    pedido_item = models.ForeignKey(
        PedidoItem,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1_000_000)],
        default=0,
    )
    cancelado = models.BooleanField(
        default=False,
    )
    inserido_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OP {self.numero} / {self.pedido_item}"

    class Meta:
        db_table = "po2_op"
        verbose_name = "Ordem de produção"
        verbose_name_plural = "Ordens de produção"
        ordering = ['-numero']


class ApontamentoProducao(models.Model):
    admin_order = 700
    op = models.ForeignKey(
        OrdemProducao,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    qtd_perda = models.IntegerField(
        'quantidade de perda',
        validators=[MinValueValidator(0), MaxValueValidator(1_000_000)],
        default=0,
    )
    qtd_prod = models.IntegerField(
        'quantidade produzida',
        validators=[MinValueValidator(0), MaxValueValidator(1_000_000)],
        default=0,
    )
    apontado_em = models.DateTimeField(auto_now_add=True)
    encerrado = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"OP {self.op.numero} +{self.qtd_prod} -{self.qtd_perda} {self.apontado_em:%d/%m/%Y %H:%M:%S}"

    class Meta:
        db_table = "po2_aponta_prod"
        verbose_name = "Apontamento de produção"
        verbose_name_plural = "Apontamentos de produção"
        ordering = ['-op_id', 'apontado_em']
