# Generated by Django 4.1.7 on 2023-09-15 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0047_alter_cliente_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='apelido',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]