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

    foto_perfil = models.ImageField('Imagen', upload_to='perfil/',  default='perfil/usuario_default.png' ,max_length=255, null=True, blank=True)
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
    nombre_actor = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    biografia = models.TextField()
    nacionalidad= models.CharField(max_length=30)


class Genero(models.Model):
    nombre_genero = models.CharField(max_length=30)
    descripcion_genero = models.CharField(max_length=300)