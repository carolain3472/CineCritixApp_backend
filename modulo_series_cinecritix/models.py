from django.db import models
from users_cinecritix.models import *

# Create your models here.

#_______________________________________________________________________________________________________

class Serie(models.Model):

    imagen_serie= models.ImageField('Imagen', upload_to='series/' ,max_length=10000, null=True, blank=True)
    titulo_serie = models.CharField(unique=True, max_length=30, blank=False, null=False)
    director_serie = models.CharField(max_length=30, blank=False, null=False)
    sipnosis_serie = models.CharField(max_length=250, blank=False, null=False)
    fecha_estreno_serie = models.DateField()
    generos = models.ManyToManyField(Genero, related_name='generos_serie')
    actores = models.ManyToManyField(Actor, related_name='series_actuadas')
    link_serie = models.TextField(null= True, blank= True,  default="No se encontró link")
    link_trailer = models.TextField(null= True, blank= True,  default="No se encontró link")

    def __str__(self):
        return self.titulo_serie
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
    imagen_temporada = models.ImageField('Imagen', upload_to='temporada/', max_length=10000, null=True, blank=True)
    nombre_temporada = models.ForeignKey(Serie, on_delete=models.CASCADE, null=False, related_name='temporadas_nombre')
    id_serie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=False, related_name='temporadas_id')
    sipnosis_temporada = models.CharField(max_length=250, blank=False, null=False)
    capitulos_temporada = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.nombre_temporada.titulo_serie

#----------------------------------------------------------------------------------------

class Capitulo(models.Model):

    id_temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, null=False)
    titulo_capitulo = models.CharField(max_length=250, blank=False, null=False)
    numero_capitulo = models.IntegerField(null=False, blank=False, default=0)
    sipnosis_capitulo = models.CharField(max_length=250, blank=False, null=False)
    duracion_capitulo = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.titulo_capitulo


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
    
