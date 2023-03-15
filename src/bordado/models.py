from django.db import models


__all__ = ['Empresa', 'Cliente']


class Empresa(models.Model):
    nome = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        db_table = "po2_empresa"
        verbose_name = "Empresa"
        ordering = ['nome']


class Cliente(models.Model):
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
    )
    nome = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        db_table = "po2_cliente"
        verbose_name = "Cliente"
        ordering = ['nome']
