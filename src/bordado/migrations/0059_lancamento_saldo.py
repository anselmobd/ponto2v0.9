# Generated by Django 4.1.7 on 2023-12-03 17:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0058_lancamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='lancamento',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(-1000000), django.core.validators.MaxValueValidator(1000000)]),
        ),
    ]
