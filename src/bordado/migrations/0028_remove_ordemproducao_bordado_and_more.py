# Generated by Django 4.1.7 on 2023-04-26 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0027_pedidoitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordemproducao',
            name='bordado',
        ),
        migrations.RemoveField(
            model_name='ordemproducao',
            name='cliente',
        ),
        migrations.DeleteModel(
            name='ApontamentoProducao',
        ),
        migrations.DeleteModel(
            name='OrdemProducao',
        ),
    ]
