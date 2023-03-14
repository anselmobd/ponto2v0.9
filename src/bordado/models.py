from django.db import models


class Empresa(models.Model):
    nome = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        db_table = "po2_empresa"
        verbose_name = "Empresa"
