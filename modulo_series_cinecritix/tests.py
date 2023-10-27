from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Serie
from users_cinecritix.models import *
from modulo_series_cinecritix import *
from users_cinecritix.serializer import ActorSerializer
from .serializer import SerieSerializer, CapituloSerializer
from .models import *
from .models import Temporada, Capitulo, Puntuacion_serie, Favorito_serie, Comentarios_serie

# Create your tests here.
class TusPruebas(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.registered_user = self.create_registered_user()
        
        # Crear actores
        self.actor1 = Actor.objects.create(nombre_actor='Actor 1', fecha_nacimiento='1990-01-01', biografia='Biografía Actor 1', nacionalidad='Nacionalidad Actor 1')
        self.actor2 = Actor.objects.create(nombre_actor='Actor 2', fecha_nacimiento='1985-03-15', biografia='Biografía Actor 2', nacionalidad='Nacionalidad Actor 2')
        self.actor3 = Actor.objects.create(nombre_actor='Actor 3', fecha_nacimiento='1975-03-5', biografia='Biografía Actor 3', nacionalidad='Nacionalidad Actor 3')
        self.actor4 = Actor.objects.create(nombre_actor='Actor 4', fecha_nacimiento='1975-04-5', biografia='Biografía Actor 4', nacionalidad='Nacionalidad Actor 4')
        self.actor5 = Actor.objects.create(nombre_actor='Actor 5', fecha_nacimiento='1956-03-5', biografia='Biografía Actor 5', nacionalidad='Nacionalidad Actor 5')
        self.actor6 = Actor.objects.create(nombre_actor='Actor 6', fecha_nacimiento='1935-04-5', biografia='Biografía Actor 6', nacionalidad='Nacionalidad Actor 6')
        
        # Crear géneros
        self.genero1 = Genero.objects.create(nombre_genero='Drama', descripcion_genero='Descripción Drama')
        self.genero2 = Genero.objects.create(nombre_genero='Comedia', descripcion_genero='Descripción Comedia')
        self.genero3 = Genero.objects.create(nombre_genero='Terror', descripcion_genero='Descripción Terror')
        self.genero4 = Genero.objects.create(nombre_genero='Suspenso', descripcion_genero='Descripción Suspenso')

        
        self.sample_serie = Serie.objects.create(
            titulo_serie='Ejemplo de película',
            director_serie='Director de ejemplo',
            sipnosis_serie='Sinopsis de ejemplo',
            fecha_estreno_serie='2023-01-01',

        )
        self.sample_serie.actores.set([ self.actor1,  self.actor2,  self.actor3,  self.actor4])
        self.sample_serie.generos.set([self.genero1, self.genero2])

        self.sample_temporada = Temporada.objects.create(
            id_serie=self.sample_serie,
            sipnosis_temporada='Sinopsis de la temporada',
            capitulos_temporada=10,  # Define la cantidad de capítulos que desees
  )
        
        self.sample2_temporada = Temporada.objects.create(
            id_serie=self.sample_serie,
            sipnosis_temporada='Sinopsis de la temporada2',
            capitulos_temporada=12,  # Define la cantidad de capítulos que desees
  )
        
        self.sample_capitulo = Capitulo.objects.create(
            id_temporada = self.sample2_temporada,
            titulo_capitulo = "Capitulo. Niebla oscura",
            numero_capitulo = 1,
            sipnosis_capitulo = "Es un capitulo excelente",
            duracion_capitulo = 25,
        )

        self.sample4_capitulo = Capitulo.objects.create(
            id_temporada = self.sample2_temporada,
            titulo_capitulo = "Capitulo3. Niebla oscura",
            numero_capitulo = 1,
            sipnosis_capitulo = "Es un capitulo excelente",
            duracion_capitulo = 25,
        )
        

    def create_registered_user(self):
        # Crear un usuario registrado para utilizar en la prueba de inicio de sesión
        User = CustomUser
        registered_user = User.objects.create_superuser(
            nombre='Tatiana',
            documento= '1234567',
            email='test@example.com',
            password='password'
        )
        return registered_user

#______________series___________________________________________________________________________
    def test_crear_serie(self):
        url = reverse('series:crear_serie')  # Asegúrate de configurar las URLs en tu aplicación
        data = {
            'titulo_serie': 'Nueva serie',
            'director_serie': 'Nuevo director',
            'sipnosis_serie': 'Nueva sinopsis',
            'fecha_estreno_serie': '2024-01-01',
            'generos': [self.genero1.id, self.genero2.id],  # Asignar géneros a la serie
            'actores': [self.actor1.id, self.actor2.id],  # Asignar actores a la serie

        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Serie.objects.count(), 2)

    def test_creacion_serie_fallida(self):
        url =  reverse('series:crear_serie')  # Asegúrate de que esta sea la URL correcta
        data = {
            'titulo_serie': 'Nueva serie',
            'director_serie': 'Nuevo director',
        }  # Datos insuficientes para una creación exitosa

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)

    def test_crear_puntuacion_serie_con_datos_validos(self):
        url = reverse('series:crear_puntuacion_serie') 
        data_valida = {
            'usuario': self.registered_user.id,  
            'serie': self.sample_serie.id,
            'fecha': '2023-10-22',
            'puntuacion': 7,  
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 201)
    
    ##Esta me dice que Falló
    def test_crear_puntuacion_serie_con_datos_invalidos(self):
        url = reverse('series:crear_puntuacion_serie') 
        data_valida = {
            'usuario': 5,   #Id, usuario inexistente
            'serie': self.sample_serie.id,
            'fecha': '2023-10-22',
            'puntuacion': 'A',  #Puntuacion invalida
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 400)

    def test_agregar_serie_favoritos_con_datos_validos(self):
        url = reverse('series:agregar_favorita_serie') 
        data_valida = {
            'usuario': self.registered_user.id,
            'serie': [self.sample_serie.id],  # Utiliza el nombre de campo correcto, que es "serie"
            'fecha': '2023-10-22',
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 201)

    def test_agregar_serie_favoritos_con_datos_invalidos(self):
        url = reverse('series:agregar_favorita_serie') 
        data_valida = {
            'usuario': 5,  # Un usuario que no existe
            'serie': 2, #Una serie que no existe
            'fecha': '2023-10-22',
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 400)

        #Test crear comentario de serie

    def test_agregar_serie_comentario_con_datos_validos(self):
        url = reverse('series:agregar_comentario_serie') 
        data_valida = {
            'usuario': self.registered_user.id,  
            'serie': self.sample_serie.id,
            'fecha': '2023-10-22',
            'comentario': 'Hola, esto es un comentario'
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 201)

    def test_agregar_serie_comentario_con_datos_invalidos(self):
        url = reverse('series:agregar_comentario_serie') 
        data_valida = {
            'usuario': 7,  
            'serie': self.sample_serie.id,
            'fecha': '2023-10-22',
            'comentario': 'Hola, esto es un comentario'
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 400)

        
        #Test crear puntaje global de serie
    def test_promedio_puntuacion_serie_con_puntuaciones(self):

        # Crear algunas puntuaciones
        Puntuacion_serie.objects.create(usuario= self.registered_user, serie=self.sample_serie, fecha='2023-10-22', puntuacion=4)
        Puntuacion_serie.objects.create(usuario= self.registered_user , serie=self.sample_serie, fecha='2023-10-22', puntuacion=5)
        Puntuacion_serie.objects.create(usuario= self.registered_user , serie=self.sample_serie, fecha='2023-10-22', puntuacion=3)

        url = reverse('series:promedio_total_puntuacion_serie', args=[self.sample_serie.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['promedio'], 4.0)

        #Test list

        """     def test_listar_series_favoritas_usuario(self):
        Favorito_serie.objects.create(usuario=self.registered_user,serie= self.sample_serie, fecha='2023-10-22')

        url = reverse('series:listar_series_favoritas_usuario', args=[self.registered_user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1) """


    def test_listar_comentarios_series_usuario(self):
        Comentarios_serie.objects.create(usuario=self.registered_user, serie=self.sample_serie, fecha= '2023-10-22', comentario="Un buen comentario")

        url = reverse('series:listar_comentarios_series_usuario', args=[self.registered_user.id])
        response = self.client.get(url)
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_listar_comentarios_serie(self):
        Comentarios_serie.objects.create(usuario=self.registered_user, serie=self.sample_serie, fecha= '2023-10-22', comentario="Un buen comentario")
        Comentarios_serie.objects.create(usuario=self.registered_user, serie=self.sample_serie, fecha= '2023-10-22', comentario="Un mal comentario")

        url = reverse('series:listar_comentarios_serie', args=[self.sample_serie.id])
        response = self.client.get(url)
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_listar_todas_las_series(self):
        url = reverse("series:listar_todas_series")
        response = self.client.get(url)
        series = Serie.objects.all()
        serializer = SerieSerializer(series, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    
    def test_listar_actores_de_serie(self):
        url = reverse("series:listar_actores_de_serie", args=[self.sample_serie.id])
        response = self.client.get(url)
        actores = self.sample_serie.actores.all()
        serializer = ActorSerializer(actores, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_filtrar_series_por_actor(self):
        url = reverse("series:filtrar_series_actor", args=[self.actor1.id])
        response = self.client.get(url)
        series = Serie.objects.filter(actores=self.actor1)
        serializer = SerieSerializer(series, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_filtrar_series_por_genero(self):
        url = reverse("series:filtrar_series_genero", args=[self.genero1.id])
        response = self.client.get(url)
        serie = Serie.objects.filter(generos=self.genero1)
        serializer = SerieSerializer(serie, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

#________________________CAPITULOS_________________________________________________________

    def test_crear_temporada(self):
        url = reverse('series:crear_capitulo')  
        data = {
            'id_temporada': self.sample2_temporada.id,
            'titulo_capitulo': 'Titulo del capitulo',
            'numero_capitulo': 3,
            'sipnosis_capitulo': "Sinopsis del capitulo", 
            'duracion_capitulo':120
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_crear_puntuacion_capitulo(self):
        url = reverse('series:crear_puntuacion_capitulo') 
        
        data_valida = {
            'usuario': self.registered_user.id,  
            'capitulo': self.sample_capitulo.id,
            'fecha': '2023-10-22',
            'puntuacion': 3,  
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 201)

    def test_agregar_capitulo_favorito(self):
        url = reverse('series:agregar_favorita_capitulo') 
        data_valida = {
            'usuario': self.registered_user.id,
            'capitulo': [self.sample_capitulo.id],  # Utiliza el nombre de campo correcto, que es "serie"
            'fecha': '2023-10-5',
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 201)
        
    def test_agregar_capitulo_comentario(self):
        url = reverse('series:agregar_comentario_capitulo') 
        data_valida = {
            'usuario': self.registered_user.id,  
            'capitulo': self.sample_capitulo.id,
            'fecha': '2023-10-22',
            'comentario': 'Hola, esto es un comentario del capitulo'
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 201)

    def test_listar_comentarios_por_capitulo(self):
        # Asegúrate de tener un capítulo de prueba en la base de datos
        
        Comentarios_capitulo.objects.create(usuario= self.registered_user,capitulo=self.sample_capitulo, fecha= '2023-10-22',comentario="Comentario 1")
        Comentarios_capitulo.objects.create(usuario= self.registered_user,capitulo=self.sample_capitulo, fecha= '2023-10-22',comentario="Comentario 2")


        url = reverse('series:listar_comentarios_capitulo', args=[self.sample_capitulo.id]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_filtrar_por_nombre_de_capitulo(self):
        # Asegúrate de tener capítulos de prueba en la base de datos

        url = reverse('series:filtrar_titulo_capitulo', args=["Capitulo3"]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['titulo_capitulo'], "Capitulo3. Niebla oscura")

    def test_promedio_puntuacion_capitulo_con_puntuaciones(self):

        # Crear algunas puntuaciones
        Puntuacion_capitulo.objects.create(usuario= self.registered_user,capitulo=self.sample4_capitulo, fecha='2023-10-22', puntuacion=6)
        Puntuacion_capitulo.objects.create(usuario= self.registered_user ,capitulo=self.sample4_capitulo, fecha='2023-10-22', puntuacion=3)
        Puntuacion_capitulo.objects.create(usuario= self.registered_user ,capitulo=self.sample4_capitulo, fecha='2023-10-22', puntuacion=1)

        url = reverse('series:promedio_total_puntuacion_capitulo', args=[self.sample4_capitulo.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        
    """     def test_listar_peliculas_favoritas_usuario(self):

        Favorito_capitulo.objects.create(usuario=self.registered_user, capitulo=self.sample_capitulo, fecha='2023-10-22')

        url = reverse('series:listar_capitulo_favoritas_usuario', args=[self.registered_user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)   """
    
    def test_listar_comentarios_capitulos_usuario(self):
        Comentarios_capitulo.objects.create(usuario=self.registered_user, capitulo=self.sample4_capitulo, fecha= '2023-10-22', comentario="Un buen comentario")

        url = reverse('series:listar_comentarios_capitulo_usuario', args=[self.registered_user.id])
        response = self.client.get(url)
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    

    



   

#________________________TEMPORADA_________________________________________________________
    def test_crear_temporada(self):
        url = reverse('series:crear_temporada')  # Asegúrate de configurar las URLs en tu aplicación
        data = {
            'id_serie': self.sample_serie.id,
            'sipnosis_temporada': 'Sinopsis de la temporada',
            'capitulos_temporada': 3,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_listar_temporadas_de_serie(self):
        # Obtiene el ID de la serie
        serie_id = self.sample_serie.id

        url = reverse('series:listar_temporadas_de_serie', args=[serie_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  # Asegúrate de ajustar esto al número real de temporadas que esperas
        