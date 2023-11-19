from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import *
from users_cinecritix.models import *
from modulo_peliculas_cinecritix import *
from .serializer import PeliculaSerializer
from users_cinecritix.serializer import ActorSerializer

class PruebasPeliculas(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.registered_user = self.create_registered_user()
        
        # Crear actores
        self.actor1 = Actor.objects.create(nombre_actor='Actor 1', fecha_nacimiento='1990-01-01', biografia='Biografía Actor 1', nacionalidad='Nacionalidad Actor 1')
        self.actor2 = Actor.objects.create(nombre_actor='Actor 2', fecha_nacimiento='1985-03-15', biografia='Biografía Actor 2', nacionalidad='Nacionalidad Actor 2')
        self.actor3 = Actor.objects.create(nombre_actor='Actor 3', fecha_nacimiento='1975-03-5', biografia='Biografía Actor 3', nacionalidad='Nacionalidad Actor 3')
        self.actor4 = Actor.objects.create(nombre_actor='Actor 4', fecha_nacimiento='1975-04-5', biografia='Biografía Actor 4', nacionalidad='Nacionalidad Actor 4')
        
        # Crear géneros
        self.genero1 = Genero.objects.create(nombre_genero='Drama', descripcion_genero='Descripción Drama')
        self.genero2 = Genero.objects.create(nombre_genero='Comedia', descripcion_genero='Descripción Comedia')
        
        self.sample_pelicula = Pelicula.objects.create(
            titulo_pelicula='Ejemplo de película',
            director_pelicula='Director de ejemplo',
            sipnosis_pelicula='Sinopsis de ejemplo',
            duracion_pelicula=120,
            fecha_estreno_pelicula='2023-01-01',
        )
        
        self.sample2_pelicula = Pelicula.objects.create(
            titulo_pelicula='Ejemplo de película2',
            director_pelicula='Director de ejemplo2',
            sipnosis_pelicula='Sinopsis de ejemplo2',
            duracion_pelicula=120,
            fecha_estreno_pelicula='2023-01-01',
        )

        self.sample2_pelicula.actores.set([ self.actor1,  self.actor2,  self.actor3,  self.actor4])
        self.sample2_pelicula.genero.set([self.genero1, self.genero2])
    

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

    def test_crear_pelicula(self):
        url = reverse('peliculas:crear_pelicula')  # Asegúrate de configurar las URLs en tu aplicación
        data = {
            'titulo_pelicula': 'Nueva película',
            'director_pelicula': 'Nuevo director',
            'sipnosis_pelicula': 'Nueva sinopsis',
            'duracion_pelicula': 90,
            'fecha_estreno_pelicula': '2024-01-01',
            'actores': [self.actor1.id, self.actor2.id],  # Asignar actores a la película
            'genero': [self.genero1.id, self.genero2.id],  # Asignar géneros a la película
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pelicula.objects.count(), 3)

    def test_creacion_pelicula_fallida(self):
        url = reverse('peliculas:crear_pelicula')  # Asegúrate de que esta sea la URL correcta
        data = {
            'titulo_pelicula': 'Nueva película',
            'director_pelicula': 'Nuevo director',
        }  # Datos insuficientes para una creación exitosa

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)


    def test_crear_puntuacion_pelicula_con_datos_validos(self):
        url = reverse('peliculas:crear_puntuacion_pelicula') 
        data_valida = {
            'usuario': self.registered_user.id,  
            'pelicula': self.sample_pelicula.id,
            'fecha': '2023-10-22',
            'puntuacion': 7,  
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_crear_puntuacion_pelicula_con_datos_invalidos(self):
        url = reverse('peliculas:crear_puntuacion_pelicula') 
        data_valida = {
            'usuario': 5,   #Id, usuario inexistente
            'pelicula': self.sample_pelicula.id,
            'fecha': '2023-10-22',
            'puntuacion': 'A',  #Puntuacion invalida
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 400)

    def test_agregar_pelicula_favoritos_con_datos_validos(self):
        url = reverse('peliculas:agregar_favorita_pelicula') 
        data_valida = {
            'usuario': self.registered_user.id,
            'pelicula': self.sample_pelicula.id,  # Utiliza el nombre de campo correcto, que es "pelicula"
            'fecha': '2023-10-22',
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 201)


    def test_agregar_pelicula_favoritos_con_datos_invalidos(self):
        url = reverse('peliculas:agregar_favorita_pelicula') 
        data_valida = {
            'usuario': 5,  # Un usuario que no existe
            'pelicula': 2, #Una pelicula que no existe
            'fecha': '2023-10-22',
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 400)

    def test_agregar_pelicula_comentario_con_datos_validos(self):
        url = reverse('peliculas:agregar_comentario_pelicula') 
        data_valida = {
            'usuario': self.registered_user.id,  
            'pelicula': self.sample_pelicula.id,
            'fecha': '2023-10-22',
            'comentario': 'Hola, esto es un comentario'
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 201)

    def test_agregar_pelicula_comentario_con_datos_invalidos(self):
        url = reverse('peliculas:agregar_comentario_pelicula') 
        data_valida = {
            'usuario': 7,  
            'pelicula': self.sample_pelicula.id,
            'fecha': '2023-10-22',
            'comentario': 'Hola, esto es un comentario'
        }
        response = self.client.post(url, data_valida, format='json')
        self.assertEqual(response.status_code, 400)

    def test_promedio_puntuacion_pelicula_con_puntuaciones(self):

        # Crear algunas puntuaciones
        Puntuacion_pelicula.objects.create(usuario= self.registered_user,pelicula=self.sample_pelicula, fecha='2023-10-22', puntuacion=4)
        Puntuacion_pelicula.objects.create(usuario= self.registered_user ,pelicula=self.sample_pelicula, fecha='2023-10-22', puntuacion=5)
        Puntuacion_pelicula.objects.create(usuario= self.registered_user ,pelicula=self.sample_pelicula, fecha='2023-10-22', puntuacion=3)

        url = reverse('peliculas:promedio_total_puntuacion_pelicula', args=[self.sample_pelicula.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['promedio'], 4.0)

    def test_listar_peliculas_favoritas_usuario(self):

        Favorito_pelicula.objects.create(usuario=self.registered_user, pelicula=self.sample_pelicula, fecha='2023-10-22')

        url = reverse('peliculas:listar_peliculas_favoritas_usuario', args=[self.registered_user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  


    def test_listar_comentarios_peliculas_usuario(self):
        Comentarios_pelicula.objects.create(usuario=self.registered_user, pelicula=self.sample_pelicula, fecha= '2023-10-22', comentario="Un buen comentario")

        url = reverse('peliculas:listar_comentarios_peliculas_usuario', args=[self.registered_user.id])
        response = self.client.get(url)
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_listar_comentarios_pelicula(self):
        Comentarios_pelicula.objects.create(usuario=self.registered_user, pelicula=self.sample_pelicula, fecha= '2023-10-22', comentario="Un buen comentario")
        Comentarios_pelicula.objects.create(usuario=self.registered_user, pelicula=self.sample_pelicula, fecha= '2023-10-22', comentario="Un mal comentario")

        url = reverse('peliculas:listar_comentarios_pelicula', args=[self.sample_pelicula.id])
        response = self.client.get(url)
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_listar_todas_las_peliculas(self):
        url = reverse("peliculas:listar_todas_peliculas")
        response = self.client.get(url)
        peliculas = Pelicula.objects.all()
        serializer = PeliculaSerializer(peliculas, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_listar_actores_de_pelicula(self):
        url = reverse("peliculas:listar_actores_de_pelicula", args=[self.sample2_pelicula.id])
        response = self.client.get(url)
        actores = self.sample2_pelicula.actores.all()
        serializer = ActorSerializer(actores, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_filtrar_peliculas_por_actor(self):
        url = reverse("peliculas:filtrar_peliculas_actor", args=[self.actor1.id])
        response = self.client.get(url)
        peliculas = Pelicula.objects.filter(actores=self.actor1)
        serializer = PeliculaSerializer(peliculas, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_filtrar_peliculas_por_genero(self):
        url = reverse("peliculas:filtrar_peliculas_genero", args=[self.genero1.id])
        response = self.client.get(url)
        peliculas = Pelicula.objects.filter(genero=self.genero1)
        serializer = PeliculaSerializer(peliculas, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)