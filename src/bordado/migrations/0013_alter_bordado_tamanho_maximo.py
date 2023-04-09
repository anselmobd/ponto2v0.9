# Generated by Django 4.1.7 on 2023-04-09 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0012_bordado_cores_bordado_pontos_bordado_tamanho_maximo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bordado',
            name='tamanho_maximo',
            field=models.PositiveIntegerField(default=0, help_text='em milímetros', verbose_name='tamanho máximo'),
        ),
    ]
