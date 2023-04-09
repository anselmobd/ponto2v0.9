# Generated by Django 4.1.7 on 2023-04-09 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0011_dificuldadebordado'),
    ]

    operations = [
        migrations.AddField(
            model_name='bordado',
            name='cores',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bordado',
            name='pontos',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bordado',
            name='tamanho_maximo',
            field=models.PositiveIntegerField(default=0, verbose_name='tamanho máximo'),
        ),
    ]
