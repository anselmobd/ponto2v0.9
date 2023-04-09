from django.db import models


__all__ = ['Empresa', 'Cliente', 'Bordado']


class Empresa(models.Model):
    nome = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        db_table = "po2_empresa"
        verbose_name = "Empresa"
        ordering = ['nome']


class Cliente(models.Model):
    # empresa = models.ForeignKey(
    #     Empresa,
    #     on_delete=models.PROTECT,
    # )
    nome = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        db_table = "po2_cliente"
        verbose_name = "Cliente"
        ordering = ['nome']
        # unique_together = [['empresa', 'nome']]


class Bordado(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
    )
    nome = models.CharField(
        max_length=50,
    )

    # número de pontos, 
    # número de cores, 
    # tamanho, 
    # dificuldade

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        db_table = "po2_bordado"
        verbose_name = "Bordado"
        ordering = ['nome']
        unique_together = [['cliente', 'nome']]
