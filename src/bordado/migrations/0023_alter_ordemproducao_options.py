# Generated by Django 4.1.7 on 2023-04-13 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0022_alter_ordemproducao_options_ordemproducao_bordado_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordemproducao',
            options={'ordering': ['-numero'], 'verbose_name': 'Ordem de produção', 'verbose_name_plural': 'Ordens de produção'},
        ),
    ]
