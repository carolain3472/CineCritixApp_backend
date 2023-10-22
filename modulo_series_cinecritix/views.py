from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Serie, Puntuacion_serie, Favorito_serie, Comentarios_serie, Temporada, Capitulo, Puntuacion_capitulo, Favorito_capitulo, Comentarios_capitulo
from .serializer import SerieSerializer, TemporadaSerializer, CapituloSerializer, PuntuacionSerieSerializer, FavoritoSerieSerializer, ComentarioSerieSerializer, PuntuacionCapituloSerializer, FavoritoCapituloSerializer, ComentarioCapituloSerializer

class Crear_serie(APIView):
    def post(self, request):
        datos = request.data
        serializer = SerieSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Crear_puntuacion_serie(APIView):
    def post(self, request):
        datos = request.data
        serializer = PuntuacionSerieSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class promedio_total_puntuacioon_serie(APIView):
    def get(self, request, serie_id):
        puntuaciones = Puntuacion_serie.objects.filter(serie=serie_id)
        total_puntuaciones = puntuaciones.count()
        if total_puntuaciones == 0:
            promedio = 0
        else:
            suma_puntuaciones = sum([p.puntuacion for p in puntuaciones])
            promedio = suma_puntuaciones / total_puntuaciones

        return Response({'promedio': promedio}, status=status.HTTP_200_OK)

class Agregar_serie_favoritos(APIView):
    def post(self, request):
        datos = request.data
        serializer = FavoritoSerieSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Agregar_comentario_serie(APIView):
    def post(self, request):
        datos = request.data
        serializer = ComentarioSerieSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class listar_todos_comentarios_serie(APIView):
    def get(self, request, serie_id):
        comentarios = Comentarios_serie.objects.filter(serie=serie_id)
        serializer = ComentarioSerieSerializer(comentarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class listar_serie_favoritas_usuario(APIView):
    def get(self, request, usuario_id):
        favoritas = Favorito_serie.objects.filter(usuario=usuario_id)
        serie = [fav.serie for fav in favoritas]
        serializer = SerieSerializer(serie, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class listar_comentarios_serie_usuario(APIView):
    def get(self, request, usuario_id):
        comentarios = Comentarios_pelicula.objects.filter(usuario=usuario_id)
        serializer = ComentarioSerieSerializer(comentarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# A partir de acá no sé si está correcto porque son funciones que no habia para Peliculas 
# En este caso es para Capitulos y Temporadas
# Perdón si está malo

class Crear_capitulo(APIView):
    def post(self, request):
        datos = request.data
        serializer = CapituloSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Crear_puntuacion_capitulo(APIView):
    def post(self, request):
        datos = request.data
        serializer = PuntuacionCapituloSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Agregar_capitulo_favoritos(APIView):
    def post(self, request):
        datos = request.data
        serializer = FavoritoCapituloSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Agregar_comentario_capitulo(APIView):
    def post(self, request):
        datos = request.data
        serializer = ComentarioCapituloSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class listar_todos_comentarios_capitulo(APIView):
    def get(self, request, serie_id):
        comentarios = Comentarios_capitulo.objects.filter(capitulo=capitulo_id)
        serializer = ComentarioCapituloSerializer(comentarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class listar_capitulo_favoritas_usuario(APIView):
    def get(self, request, usuario_id):
        favoritas = Favorito_capitulo.objects.filter(usuario=usuario_id)
        capitulo = [fav.capitulo for fav in favoritas]
        serializer = CapituloSerializer(capitulo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class listar_comentarios_capitulo_usuario(APIView):
    def get(self, request, usuario_id):
        comentarios = Comentarios_capitulo.objects.filter(usuario=usuario_id)
        serializer = ComentarioCapituloSerializer(comentarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class promedio_total_puntuacioon_capitulo(APIView):
    def get(self, request, serie_id):
        puntuaciones = Puntuacion_capitulo.objects.filter(capitulo=capitulo_id)
        total_puntuaciones = puntuaciones.count()
        if total_puntuaciones == 0:
            promedio = 0
        else:
            suma_puntuaciones = sum([p.puntuacion for p in puntuaciones])
            promedio = suma_puntuaciones / total_puntuaciones

        return Response({'promedio': promedio}, status=status.HTTP_200_OK)

class Crear_temporada(APIView):
    def post(self, request):
        datos = request.data
        serializer = TemporadaSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)