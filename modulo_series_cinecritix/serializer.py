from rest_framework import serializers
from .models import *


class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serie
        fields = '__all__'

class TemporadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temporada
        fields = '__all__'

class CapituloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitulo
        fields = '__all__'

class PuntuacionSerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puntuacion_serie
        fields = '__all__'

class FavoritoSerieSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Favorito_serie
        fields = '__all__'

   

class ComentarioSerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentarios_serie
        fields = '__all__'


class PuntuacionCapituloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puntuacion_capitulo
        fields = '__all__'

class FavoritoCapituloSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Favorito_capitulo
        fields = '__all__'

class ComentarioCapituloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentarios_capitulo
        fields = '__all__'



