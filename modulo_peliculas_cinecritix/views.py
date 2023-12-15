from turtle import pd
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Pelicula, Puntuacion_pelicula, Favorito_pelicula, Comentarios_pelicula
from .serializer import PeliculaSerializer, PuntuacionPeliculaSerializer, FavoritoPeliculaSerializer, ComentariosPeliculaSerializer
from users_cinecritix.serializer import ActorSerializer
from users_cinecritix.models import Actor, Genero


class Crear_pelicula(APIView):
    def post(self, request):
        datos = request.data
        serializer = PeliculaSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Promedio_total_puntuacioon_pelicula(APIView):
    def get(self, request, pelicula_id):
        puntuaciones = Puntuacion_pelicula.objects.filter(pelicula=pelicula_id)
        total_puntuaciones = puntuaciones.count()
        if total_puntuaciones == 0:
            promedio = 0
        else:
            suma_puntuaciones = sum([p.puntuacion for p in puntuaciones])
            promedio = suma_puntuaciones / total_puntuaciones

        return Response({'promedio': promedio}, status=status.HTTP_200_OK)


class Crear_puntuacion_pelicula(APIView):
    def post(self, request):
        datos = request.data
        serializer = PuntuacionPeliculaSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class listar_todos_comentarios_pelicula(APIView):
    def get(self, request, pelicula_id):
        comentarios = Comentarios_pelicula.objects.filter(pelicula=pelicula_id)
        serializer = ComentariosPeliculaSerializer(comentarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Agregar_pelicula_favoritos(APIView):
    def post(self, request):
        datos = request.data
        serializer = FavoritoPeliculaSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Agregar_comentario_pelicula(APIView):
    def post(self, request):
        datos = request.data
        serializer = ComentariosPeliculaSerializer(data=datos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Listar_peliculas_favoritas_usuario(APIView):
    def get(self, request, usuario_id):
        favoritas = Favorito_pelicula.objects.filter(usuario=usuario_id)
        peliculas = [fav.pelicula for fav in favoritas]
        serializer = PeliculaSerializer(peliculas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class listar_comentarios_peliculas_usuario(APIView):
    def get(self, request, usuario_id):
        comentarios = Comentarios_pelicula.objects.filter(usuario=usuario_id)
        serializer = ComentariosPeliculaSerializer(comentarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ListarTodasLasPeliculas(APIView):
    def get(self, request):
        peliculas = Pelicula.objects.all()
        serializer = PeliculaSerializer(peliculas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Listar los actores de una película
class ListarActoresDePelicula(APIView):
    def get(self, request, pelicula_id):
        pelicula = Pelicula.objects.get(pk=pelicula_id)
        actores = pelicula.actores.all()
        serializer = ActorSerializer(actores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Listar todos los actores
class ListarActores(APIView):
    def get(self, request):
        actores = Actor.objects.all()
        serializer = ActorSerializer(actores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Filtrar películas por actor
class FiltrarPeliculasPorActor(APIView):
    def get(self, request, actor_id):
        actor = Actor.objects.get(pk=actor_id)
        peliculas = Pelicula.objects.filter(actores=actor)
        serializer = PeliculaSerializer(peliculas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
# Filtrar películas por género
class FiltrarPeliculasPorGenero(APIView):
    def get(self, request, genero_id):
        genero = Genero.objects.get(pk=genero_id)
        peliculas = Pelicula.objects.filter(genero=genero)
        serializer = PeliculaSerializer(peliculas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    