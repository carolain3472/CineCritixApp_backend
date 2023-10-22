from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Pelicula
from users_cinecritix.models import *
from modulo_peliculas_cinecritix import *
from .serializer import PeliculaSerializer

class TusPruebas(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.registered_user = self.create_registered_user()
        
        # Crear actores
        self.actor1 = Actor.objects.create(nombre_actor='Actor 1', fecha_nacimiento='1990-01-01', biografia='Biografía Actor 1', nacionalidad='Nacionalidad Actor 1')
        self.actor2 = Actor.objects.create(nombre_actor='Actor 2', fecha_nacimiento='1985-03-15', biografia='Biografía Actor 2', nacionalidad='Nacionalidad Actor 2')
        
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
        self.assertEqual(Pelicula.objects.count(), 2)

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
            'pelicula': self.sample_pelicula.id,
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

    