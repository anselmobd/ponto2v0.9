# Generated by Django 4.1.7 on 2023-03-15 00:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0003_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='empresa',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='bordado.empresa'),
            preserve_default=False,
        ),
    ]