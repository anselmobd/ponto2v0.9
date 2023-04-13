from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from o2lib.codes.cnpj import CNPJ


__all__ = ['Cliente', 'DificuldadeBordado', 'Bordado']


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

    @property
    def cnpj(self):
        cnpj = CNPJ()
        cnpj_str = cnpj.to_str(self.cnpj9, self.cnpj4, self.cnpj2)
        if not cnpj.valid(cnpj_str):
            cnpj_str += "!"
        return cnpj_str

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
