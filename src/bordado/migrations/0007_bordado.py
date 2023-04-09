# Generated by Django 4.1.7 on 2023-03-22 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bordado', '0006_alter_cliente_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bordado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bordado.cliente')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bordado.empresa')),
            ],
            options={
                'verbose_name': 'Bordado',
                'db_table': 'po2_bordado',
                'ordering': ['nome'],
                'unique_together': {('empresa', 'cliente', 'nome')},
            },
        ),
    ]