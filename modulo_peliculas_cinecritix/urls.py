from django.urls import path, include
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from .views import Crear_pelicula
from .views import Crear_puntuacion_pelicula
from .views import Agregar_comentario_pelicula
from .views import Agregar_pelicula_favoritos

urlpatterns = [
    path('crear_pelicula/', Crear_pelicula.as_view(), name='crear_pelicula'),
    path('crear_puntuacion_pelicula/', Crear_puntuacion_pelicula.as_view(), name='crear_puntuacion_pelicula'),
    path('agregar_favorita_pelicula/', Agregar_pelicula_favoritos.as_view(), name='agregar_favorita_pelicula'),
    path('agregar_comentario_pelicula/', Agregar_comentario_pelicula.as_view(), name='agregar_comentario_pelicula'),
]