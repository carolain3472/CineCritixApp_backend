# Generated by Django 4.2.6 on 2023-10-22 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_series_cinecritix', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serie',
            name='portada_serie',
        ),
    ]
