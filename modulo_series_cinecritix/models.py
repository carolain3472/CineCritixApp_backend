from django.db import models
from users_cinecritix.models import *

# Create your models here.

#_______________________________________________________________________________________________________

class Serie(models.Model):

    titulo_serie = models.CharField(unique=True, max_length=30, blank=False, null=False)
    director_serie = models.CharField(max_length=30, blank=False, null=False)
    sipnosis_serie = models.CharField(max_length=250, blank=False, null=False)
    fecha_estreno_serie = models.DateField()
   # portada_serie = models.ImageField()
    generos = models.ManyToManyField(Genero, related_name='generos_serie')
    actores = models.ManyToManyField(Actor, related_name='series_actuadas')
    ##link de serie 
    ##link de trailer

class Puntuacion_serie(models.Model):

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    serie= models.ForeignKey(Serie, on_delete=models.CASCADE, null=False)
    fecha= models.DateField()
    puntuacion= models.IntegerField(null=False, blank=False, default=0)

class Favorito_serie(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    serie= models.ManyToManyField(Serie, related_name='peliculas_like')
    fecha= models.DateField()


class Comentarios_serie(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    serie= models.ForeignKey(Serie, on_delete=models.CASCADE, null=False)
    fecha= models.DateField()
    comentario= models.TextField()


#-------------------------------------------------------------------------------------------------------------

class Temporada(models.Model):

    id_serie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=False)
    sipnosis_temporada = models.CharField(max_length=250, blank=False, null=False)
    capitulos_temporada = models.IntegerField(null=False, blank=False, default=0)


#----------------------------------------------------------------------------------------

class Capitulo(models.Model):

    id_temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, null=False)
    titulo_capitulo = models.CharField(max_length=250, blank=False, null=False)
    numero_capitulo = models.IntegerField(null=False, blank=False, default=0)
    sipnosis_capitulo = models.CharField(max_length=250, blank=False, null=False)
    duracion_capitulo = models.IntegerField(null=False, blank=False, default=0)


class Puntuacion_capitulo(models.Model):

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    capitulo= models.ForeignKey(Capitulo, on_delete=models.CASCADE, null=False)
    fecha= models.DateField()
    puntuacion= models.IntegerField(null=False, blank=False, default=0)

class Favorito_capitulo(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    capitulo= models.ManyToManyField(Capitulo, related_name='peliculas_like')
    fecha= models.DateField()


class Comentarios_capitulo(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    capitulo= models.ForeignKey(Capitulo, on_delete=models.CASCADE, null=False)
    fecha= models.DateField()
    comentario= models.TextField()
    
