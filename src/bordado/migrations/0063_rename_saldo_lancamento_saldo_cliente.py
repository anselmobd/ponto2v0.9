# Generated by Django 4.1.7 on 2023-12-03 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0062_alter_lancamento_cobranca'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lancamento',
            old_name='saldo',
            new_name='saldo_cliente',
        ),
    ]