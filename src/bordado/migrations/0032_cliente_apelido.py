# Generated by Django 4.1.7 on 2023-06-04 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0031_apontamentoproducao_encerrado'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='apelido',
            field=models.CharField(default='', max_length=50),
        ),
    ]
