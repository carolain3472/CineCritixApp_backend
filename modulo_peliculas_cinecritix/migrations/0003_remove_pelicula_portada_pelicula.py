# Generated by Django 4.2.6 on 2023-12-15 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_peliculas_cinecritix', '0002_pelicula_imagen_pelicula_pelicula_link_pelicula_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pelicula',
            name='portada_pelicula',
        ),
    ]
