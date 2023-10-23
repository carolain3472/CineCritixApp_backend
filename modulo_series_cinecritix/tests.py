from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Serie
from users_cinecritix.models import *
from modulo_series_cinecritix import *
from .serializer import SerieSerializer, CapituloSerializer

# Create your tests here.
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
        
        self.sample_serie = Serie.objects.create(
            titulo_serie='Ejemplo de película',
            director_serie='Director de ejemplo',
            sipnosis_serie='Sinopsis de ejemplo',
            fecha_estreno_serie='2023-01-01',

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