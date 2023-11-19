from django.urls import path, include
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('crear_serie/', Crear_serie.as_view(), name='crear_serie'),
    path('crear_puntuacion_serie/', Crear_puntuacion_serie.as_view(), name='crear_puntuacion_serie'),
    path('agregar_favorita_serie/', Agregar_serie_favoritos.as_view(), name='agregar_favorita_serie'),
    path('agregar_comentario_serie/', Agregar_comentario_serie.as_view(), name='agregar_comentario_serie'),
    #Crear puntaje global serie 
    path('promedio_total_puntuacion_serie/<int:serie_id>/', Promedio_total_puntuacioon_serie.as_view(), name='promedio_total_puntuacion_serie'),
    #usuario listar series favoritas
    path('listar_series_favoritas_usuario/<int:usuario_id>/', Listar_serie_favoritas_usuario.as_view(),name='listar_series_favoritas_usuario'),
    #usuario listar  comentarios de series realizados
    path('listar_comentarios_series_usuario/<int:usuario_id>/', Listar_comentarios_serie_usuario.as_view(),name='listar_comentarios_series_usuario'),
    #listar comentarios por series
    path('listar_comentarios_serie/<int:serie_id>/', Listar_todos_comentarios_serie.as_view(),name='listar_comentarios_serie'),
    #listar todas las series
    path('listar_todas_series/', ListarTodasLasSeries.as_view(),name='listar_todas_series'),
    #listar actores de series
    path('listar_actores_de_serie/<int:serie_id>/', ListarActoresDeSerie.as_view(),name='listar_actores_de_serie'),
    path('filtrar_series_actor/<int:actor_id>/', FiltrarSeriesPorActor.as_view(),name='filtrar_series_actor'),
    #listar serie por genero 
    path('filtrar_series_genero/<int:genero_id>/', FiltrarSeriesPorGenero.as_view(),name='filtrar_series_genero'),



#______________________________CAPITULOS_____________________________________________________________________________

    path('crear_capitulo/', Crear_capitulo.as_view(), name='crear_capitulo'),
    path('crear_puntuacion_capitulo/', Crear_puntuacion_capitulo.as_view(), name='crear_puntuacion_capitulo'),
    path('agregar_favorita_capitulo/', Agregar_capitulo_favoritos.as_view(), name='agregar_favorita_capitulo'),
    path('agregar_comentario_capitulo/', Agregar_comentario_capitulo.as_view(), name='agregar_comentario_capitulo'),
    #Crear puntaje global capitulo
    path('promedio_total_puntuacion_capitulo/<int:capitulo_id>/', Promedio_total_puntuacion_capitulo.as_view(), name='promedio_total_puntuacion_capitulo'),
    #usuario listar capitulos favoritas
    path('listar_capitulo_favoritas_usuario/<int:usuario_id>/', listar_capitulo_favoritas_usuario.as_view(),name='listar_capitulo_favoritas_usuario'),
    #usuario listar comentarios de capitulo realizados
    path('listar_comentarios_capitulo_usuario/<int:usuario_id>/', listar_comentarios_capitulo_usuario.as_view(),name='listar_comentarios_capitulo_usuario'),

    #listar comentarios por capitulo
    path('listar_comentarios_capitulo/<int:capitulo_id>/', ListarTodosComentariosCapitulo.as_view(),name='listar_comentarios_capitulo'),
    #Filtrar por nombre del capitulo 
    path('filtrar_titulo_capitulo/<str:titulo_capitulo>', FiltrarPorNombreCapitulo.as_view(),name='filtrar_titulo_capitulo'),
    


    #_________________________TEMPORADAS_______________________________________
    path('crear_temporada/', Crear_temporada.as_view(), name='crear_temporada'),
    path('listar_temporadas_de_serie/<int:serie_id>/', ListarTemporadasDeSerie.as_view(), name='listar_temporadas_de_serie'),

]