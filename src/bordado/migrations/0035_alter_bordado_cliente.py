# Generated by Django 4.1.7 on 2023-06-04 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0034_alter_cliente_apelido_alter_cliente_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bordado',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bordado.cliente'),
        ),
    ]
