from django.db import models
from users_cinecritix.models import *

# Create your models here.

class Pelicula(models.Model):

    titulo_pelicula = models.CharField(unique=True, max_length=30, blank=False, null=False)
    director_pelicula = models.CharField(max_length=30, blank=False, null=False)
    sipnosis_pelicula = models.CharField(max_length=250, blank=False, null=False)
    duracion_pelicula = models.IntegerField(null=False, blank=False, default=0)
    fecha_estreno_pelicula = models.DateField()
    portada_pelicula = models.ImageField(null=True)
    genero = models.ManyToManyField(Genero, related_name='genero_peliculas')
    actores = models.ManyToManyField(Actor, related_name='peliculas_actuadas')

    ##link de pelicula 
    ##link de trailer

class Puntuacion_pelicula(models.Model):

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    pelicula= models.ForeignKey(Pelicula, on_delete=models.CASCADE, null=False)
    fecha= models.DateField()
    puntuacion= models.IntegerField(null=False, blank=False, default=0)

class Favorito_pelicula(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pelicula=  models.ForeignKey(Pelicula, on_delete=models.CASCADE,  default=0)
    fecha= models.DateField()

class Comentarios_pelicula(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pelicula= models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    fecha= models.DateField()
    comentario= models.TextField()


