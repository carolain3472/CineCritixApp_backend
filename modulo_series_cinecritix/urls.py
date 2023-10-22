from django.urls import path, include
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from .views import Crear_serie, Crear_puntuacion_serie, Agregar_serie_favoritos, Agregar_comentario_serie, Crear_capitulo, Crear_puntuacion_capitulo, Agregar_capitulo_favoritos, Agregar_comentario_capitulo, Crear_temporada

urlpatterns = [
    path('crear_serie/', Crear_serie.as_view(), name='crear_serie'),
    path('crear_puntuacion_serie/', Crear_puntuacion_serie.as_view(), name='crear_puntuacion_serie'),
    path('agregar_favorita_serie/', Agregar_serie_favoritos.as_view(), name='agregar_favorita_serie'),
    path('agregar_comentario_serie/', Agregar_comentario_serie.as_view(), name='agregar_comentario_serie'),

    path('crear_capitulo/', Crear_capitulo.as_view(), name='crear_capitulo'),
    path('crear_puntuacion_capitulo/', Crear_puntuacion_capitulo.as_view(), name='crear_puntuacion_capitulo'),
    path('agregar_favorita_capitulo/', Agregar_capitulo_favoritos.as_view(), name='agregar_favorita_capitulo'),
    path('agregar_comentario_capitulo/', Agregar_comentario_capitulo.as_view(), name='agregar_comentario_capitulo'),

    path('crear_temporada/', Crear_temporada.as_view(), name='crear_temporada'),

]