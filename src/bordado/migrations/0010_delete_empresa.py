# Generated by Django 4.1.7 on 2023-04-09 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0009_alter_cliente_unique_together_remove_cliente_empresa'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Empresa',
        ),
    ]
