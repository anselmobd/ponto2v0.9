# Generated by Django 4.1.7 on 2023-04-09 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0008_alter_bordado_unique_together_remove_bordado_empresa'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cliente',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='empresa',
        ),
    ]
