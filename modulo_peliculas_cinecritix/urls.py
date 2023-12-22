from django.urls import path, include
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from .views import Crear_pelicula, DatosPeliculaObtener
from .views import Crear_puntuacion_pelicula
from .views import Agregar_comentario_pelicula
from .views import Agregar_pelicula_favoritos
from .views import Promedio_total_puntuacioon_pelicula
from .views import Listar_peliculas_favoritas_usuario
from .views import listar_comentarios_peliculas_usuario, listar_todos_comentarios_pelicula, ListarTodasLasPeliculas, ListarActoresDePelicula
from .views import ListarActores, FiltrarPeliculasPorActor,FiltrarPeliculasPorGenero


urlpatterns = [
    #Crea una pelicula
    path('crear_pelicula/', Crear_pelicula.as_view(), name='crear_pelicula'),

    #Un usuario crea una puntuación para una pelicula 
    path('crear_puntuacion_pelicula/', Crear_puntuacion_pelicula.as_view(), name='crear_puntuacion_pelicula'),
    #Un usuario agrega una pelicula a sus favoritos
    path('agregar_favorita_pelicula/', Agregar_pelicula_favoritos.as_view(), name='agregar_favorita_pelicula'),
    #Un usuario agrega un comentatio de una pelicula
    path('agregar_comentario_pelicula/', Agregar_comentario_pelicula.as_view(), name='agregar_comentario_pelicula'),

    #El sistema genera una puntuación global de una determinada pelicula
    path('promedio_total_puntuacion_pelicula/<int:pelicula_id>/', Promedio_total_puntuacioon_pelicula.as_view(), name='promedio_total_puntuacion_pelicula'),

    #Un usuario lista sus peliculas favoritas
    path('listar_peliculas_favoritas_usuario/<int:usuario_id>/', Listar_peliculas_favoritas_usuario.as_view(),name='listar_peliculas_favoritas_usuario'),
    #Un usuario lista los comentarios realizados en diversas peliculas
    path('listar_comentarios_peliculas_usuario/<int:usuario_id>/', listar_comentarios_peliculas_usuario.as_view(),name='listar_comentarios_peliculas_usuario'),

    #Listar todos los comentarios por pelicula
    path('listar_comentarios_pelicula/<int:pelicula_id>/', listar_todos_comentarios_pelicula.as_view(),name='listar_comentarios_pelicula'),
    #Listar todas las peliculas
    path('listar_todas_peliculas/', ListarTodasLasPeliculas.as_view(),name='listar_todas_peliculas'),
    #Listar los actores de una pelicula 
    path('listar_actores_de_pelicula/<int:pelicula_id>/', ListarActoresDePelicula.as_view(),name='listar_actores_de_pelicula'),
    #listar actores
    path('Listar_actores/', ListarActores.as_view(),name='Listar_actores'),

    path('datos-peliculas/', DatosPeliculaObtener.as_view(),name='datos_pelicula'),


    #Filtrar por actor una pelicula
    path('filtrar_peliculas_actor/<int:actor_id>/', FiltrarPeliculasPorActor.as_view(),name='filtrar_peliculas_actor'),
    #Filtrar por genero 
    path('filtrar_peliculas_genero/<int:genero_id>/', FiltrarPeliculasPorGenero.as_view(),name='filtrar_peliculas_genero'),

]
