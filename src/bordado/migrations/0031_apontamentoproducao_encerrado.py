# Generated by Django 4.1.7 on 2023-04-26 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0030_apontamentoproducao'),
    ]

    operations = [
        migrations.AddField(
            model_name='apontamentoproducao',
            name='encerrado',
            field=models.BooleanField(default=False),
        ),
    ]
