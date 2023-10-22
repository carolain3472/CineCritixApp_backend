from rest_framework import serializers
from .models import *


class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = '__all__'


class PuntuacionPeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puntuacion_pelicula
        fields = '__all__'

class FavoritoPeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Favorito_pelicula
        fields = '__all__'

class ComentariosPeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentarios_pelicula
        fields = '__all__'


