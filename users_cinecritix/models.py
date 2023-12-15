import datetime
import os
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from .utils.resetPassword import sendResetPasswordEmail
from django_rest_passwordreset.models import ResetPasswordToken
from django.utils import timezone

class MyUserManager(BaseUserManager):
    def create_user(self, documento, password, **extra_fields):
        if not documento:
            raise ValueError(' Documento de identidad es requerido')

        user = self.model(documento=documento, **extra_fields)
        if password:
            user.set_password(password)
 
        user.save()
        return user

    def create_superuser(self, documento, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        nombre = extra_fields.get('nombre')

        if not nombre:
            raise ValueError('El nombre es requerido para crear un superusuario')
        
     #   password = f"{first_name[0].upper()}{cedula}{primer_apellido[0].upper()}"
       # extra_fields['password'] = password 
        
        return self.create_user(documento, password, **extra_fields)



class CustomUser(AbstractUser):

    def validate_min_length(value):
        if len(value) < 6:
            raise ValidationError('Este campo debe contener al menos 6 dígitos')

    documento = models.TextField(unique=True, max_length=11, validators=[validate_min_length], error_messages={
        'unique': 'Ya hay un usuario registrado con este documento'
    })

    email = models.EmailField(unique=True,null=False)

    nombre = models.CharField(max_length=30, blank=True)
    apellido = models.CharField(max_length=30, blank=True)

    foto_perfil = models.ImageField('Imagen', upload_to='perfil/',  default='https://storage.googleapis.com/bucket-final-este-si-con-fe/perfil/usuario_default.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=accesocinecritixapp%40citric-chemist-406600.iam.gserviceaccount.com%2F20231130%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20231130T045050Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=59dc3ce8a51505f143a5c05c68ce6bac928ae510655e24a6263615406c7ccaeb221b0282eda5159baaf3af56514ac2a0a735c25447c6eee4180dace41c590a634522b0e6098efec80790286e53a6de66d1ccb8da01eda1da11670719500e96b61df6dbace97bb851220ae457c9d306fa5190c79c8301ad9da82e7192ae767e37d241e79b6537696f609d8ee6da00546f250266265ff737cccc1de63fb5ca9a4bbf8c4bb078c884de7bed2515f69a9675c61df7e6a891e698d6a4e3986519428d59b1f26bfae34b21dd44cfd66c79ca6a9628b1730b4172f9779dcd4beedc78274804304517a07c115766b71ce22b18dc6df346e927dd8acd78c38eb5a8e09e5a' ,max_length=10000, null=True, blank=True)
    deactivated_timestamp = models.DateTimeField(null=True, blank=True)

    username = None

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'nombre', 
        'documento'  
    ]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
        sendResetPasswordEmail(reset_password_token)

    def deactivate_user(self):
        self.deactivated_timestamp = datetime.now()
        self.save()

class Actor(models.Model):
    imagen_actor= models.ImageField('Imagen', upload_to='actores/' ,max_length=10000, null=True, blank=True)
    nombre_actor = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    biografia = models.TextField()
    nacionalidad= models.CharField(max_length=30)

class ExtendToken(models.Model):
    token = models.CharField(max_length=100)
    count_integer = models.IntegerField(default=0, verbose_name="Contador de intentos")

class Genero(models.Model):
    nombre_genero = models.CharField(max_length=30)
    descripcion_genero = models.CharField(max_length=300)