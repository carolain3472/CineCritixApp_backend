import datetime
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .serializer import UsuarioSerializer
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from .models import CustomUser, ExtendToken
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializer import UsuarioSerializer
import os
from django_rest_passwordreset.models import ResetPasswordToken
from storages.backends.gcloud import GoogleCloudStorage
import unicodedata
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django_rest_passwordreset.models import ResetPasswordToken, clear_expired, get_password_reset_token_expiry_time, \
    get_password_reset_lookup_field
from django_rest_passwordreset.serializers import EmailSerializer, PasswordTokenSerializer, ResetTokenSerializer
from django_rest_passwordreset.signals import reset_password_token_created, pre_password_reset, post_password_reset


class validar_token(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        email = request.data.get('email')
        token = request.data.get('token')
        password = request.data.get('password')

        usuario = get_object_or_404(CustomUser, email=email)

        reset_password_token = ResetPasswordToken.objects.filter(user=usuario).first()

        password_reset_token_validation_time = get_password_reset_token_expiry_time()
        now_minus_expiry_time = timezone.now() - timedelta(hours=password_reset_token_validation_time)
        clear_expired(now_minus_expiry_time)

        

        if not ExtendToken.objects.filter(token=reset_password_token.key).exists():
           
            extend_token = ExtendToken.objects.create(
                token=reset_password_token.key,
                count_integer=0
            )

        extend_token1=ExtendToken.objects.filter(token=reset_password_token.key).first()
    
        if reset_password_token.created_at <= now_minus_expiry_time:
            ExtendToken.objects.filter(token=reset_password_token.key).delete()
            reset_password_token.delete()

            return Response({"mensaje": "El token ha expirado", "contador":extend_token1.count_integer},
                            status=status.HTTP_403_FORBIDDEN)

        if reset_password_token.key != token:
         
            extend_token1.count_integer = extend_token1.count_integer + 1
            extend_token1.save()

            if extend_token1.count_integer==3:
                return Response({"mensaje": "Te queda solo un intento",  "contador":extend_token1.count_integer},
                            status=status.HTTP_409_CONFLICT)

            if extend_token1.count_integer>=4:
                ExtendToken.objects.filter(token=reset_password_token.key).delete()
                ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()
                usuario.is_active=False
                usuario.deactivated_timestamp= timezone.now()
                usuario.save()
                tiempo= usuario.deactivated_timestamp

                return Response({"mensaje": "Ya no tienes mas intentos, token eliminado",  "contador":extend_token1.count_integer},
                            status=status.HTTP_428_PRECONDITION_REQUIRED)

            return Response({"mensaje": "Fallo en obtener token",  "contador":extend_token1.count_integer},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        
        else:

            if reset_password_token.user.eligible_for_reset():
                pre_password_reset.send(sender=self.__class__, user=reset_password_token.user)
                try:
                    # validate the password against existing validators
                    validate_password(
                        password,
                        user=reset_password_token.user,
                        password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
                    )
                except ValidationError as e:
                    # raise a validation error for the serializer
                    raise exceptions.ValidationError({
                        'password': e.messages
                    })

                reset_password_token.user.set_password(password)
                reset_password_token.user.save()
                post_password_reset.send(sender=self.__class__, user=reset_password_token.user)

            # Delete all password reset tokens for this user
            ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

        return Response({"mensaje": "OK",  "contador":extend_token1.count_integer}, status=status.HTTP_200_OK)


class UsuariosList(viewsets.ModelViewSet):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        cedula_acceso = request.data.get("cedula_acceso")

        try:
            user = CustomUser.objects.get(cedula=cedula_acceso)
            token_exists = Token.objects.filter(user=user).exists()

            if token_exists and user.role=="Administrador":
                queryset = CustomUser.objects.all()

                is_active = request.data.get("is_active")
                apellido = request.data.get("apellido")
                nombre = request.data.get("nombre")
                rol = request.data.get("rol")
                cedula = request.data.get("cedula")

        
                filters = Q()

                # Agregar los filtros según los parámetros proporcionados
                if is_active is not None:
                    filters &= Q(is_active=is_active)
                if apellido:
                    filters &= Q(primer_apellido__icontains=apellido)
                if nombre:
                    filters &= Q(first_name__icontains=nombre)
                    ##o filters &= Q(nombre__startswith=nombre)
                if rol == "Consejero":
                     filters &= Q(role="Consejero")
                if rol == "Administrador":
                     filters &= Q(role="Administrador")
                if rol == "Monitor":
                     filters &= Q(role="Monitor")
                if cedula:
                    filters &= Q(cedula__startswith=cedula)
                # Aplicar los filtros a la consulta de usuarios
                queryset = queryset.filter(filters)

                serializer = UsuarioSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            pass

        return Response(status=status.HTTP_404_NOT_FOUND)
        
class Login(FormView): 
    template_name = "login_user.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('default:usuarioList1-list')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,*kwargs)

    def form_valid(self,form):
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)

        if token:
            login(self.request, form.get_user())
            return super(Login,self).form_valid(form)


""" Si el usuario está inactivo is_active==false, entonces que verifique si el tiempo de expiracion
        ya se cumplio, si no, no lo cambia. 

        ej:

        Mas de 4 intentos:
            is_active=False
            hora_activacion= datetimefield que contenga la hora y fecha
        
        Cuando haga login: 
            Si el tiemp0o ahora, es igual o posterior al tiempo en hora_activacion:
            is_active=True 
"""    
class LoginView(APIView):
    permission_classes = [AllowAny]  
    authentication_classes = [] 
        
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('contrasena')
 

        try:
            # Buscar al usuario por cédula en la base de datos
            usuario = CustomUser.objects.get(email=email)
            print(usuario)
            print(password)

            if usuario.deactivated_timestamp is not None:
                tiempo_login = timezone.now()
                diferencia_tiempo = tiempo_login - usuario.deactivated_timestamp
                diferencia_tiempo_minutos = diferencia_tiempo.total_seconds()/60

                if diferencia_tiempo_minutos > 1:
                    usuario.deactivated_timestamp = None
                    usuario.is_active = True
                    usuario.save()
                
                else:
                    return Response({"error": "El usuario está desactivado temporalmente."}, status=status.HTTP_403_FORBIDDEN)

            # Verificar la contraseña del usuario
            if usuario.check_password(password):
                # Autenticar al usuario y generar un token de autenticación
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    token, _ = Token.objects.get_or_create(user=user)
                    print(user.is_superuser)
                    user_data = {
                        'id': user.id,
                        'documento': user.documento,
                        'nombre': user.nombre,
                        'email': user.email,
                    }

                    print(user_data)
                    return Response({'valid': True, 'token': token.key, 
                                     'user_id': user.id,
                                     'user_documento': user.documento,
                                     'user_nombre': user.nombre,
                                     'user_apellido': user.apellido,
                                     'user_email': user.email,
                                     'user_profile': user.foto_perfil.name
                                     })
            
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Las credenciales proporcionadas son inválidas.')
        
        print("No existe el usuario o contra incorrecta")

        return Response({'valid': False})
    

class DatosUsuarioObtener(APIView):
    permission_classes = [AllowAny]  
    authentication_classes = [] 
        
    def post(self, request):
        email = request.data.get('email')
        try:
            # Buscar al usuario por cédula en la base de datos
            usuario = CustomUser.objects.get(email=email)

            # Obtener la URL de la imagen del almacenamiento de Google Cloud Storage
            storage = GoogleCloudStorage()
            profile_image_url = storage.url(usuario.foto_perfil.name)

            return Response({
                'valid': True,
                'user_id': usuario.id,
                'user_documento': usuario.documento,
                'user_nombre': usuario.nombre,
                'user_apellido': usuario.apellido,
                'user_email': usuario.email,
                'user_profile': profile_image_url,
            })
            
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('No existe este usuario autentificado')

        return Response({'valid': False})


class DarmeDeBaja(APIView):
    permission_classes = [AllowAny]  
    authentication_classes = [] 

    def post(self, request):
        # Suponiendo que pasas el nombre de usuario en el cuerpo de la solicitud
        email = request.data.get('email')

        # Buscar el usuario en la base de datos
        usuario = get_object_or_404(CustomUser, email=email)

        # Eliminar el usuario
        usuario.delete()

        return Response({"mensaje": f"El usuario {email} ha sido eliminado correctamente."},
                        status=status.HTTP_200_OK)
    

class UserProfileView(RetrieveAPIView):
    permission_classes = [AllowAny]  
    authentication_classes = [] 
    queryset = CustomUser.objects.all()
    serializer_class = UsuarioSerializer
    
class Saludo(APIView):
    def post(self, request):
        nombre = request.data.get('nombre')
        print(nombre)
        return Response({"mensaje": f"Hola, {nombre}!"}, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]  
    authentication_classes = []  

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        nombre = request.data.get('nombre')
        apellido = request.data.get('apellido')
        documento = request.data.get("documento")
        email = request.data.get('email')
        contrasena = request.data.get('contrasena')
        imagen_seleccionada = request.data.get('imagen_seleccionada')

        try:
            validate_email(email)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

      
        superuser = CustomUser.objects.create_superuser(
            nombre=nombre,
            apellido=apellido,
            documento=documento,
            email=email,
            password=contrasena,
            is_active= True
        )

     
        superuser.is_staff = True
        superuser.is_superuser = True

        # Si se especifica una imagen, úsala, de lo contrario, usa la imagen por defecto
        if imagen_seleccionada:
            iconos_folder = os.path.join('media', 'iconos')
            
            print(os.path.join(iconos_folder, imagen_seleccionada))
            print(os.listdir(iconos_folder))
            print(imagen_seleccionada)

            # Verifica que la imagen seleccionada esté en la carpeta de iconos
            # Verifica que la imagen seleccionada esté en la carpeta de iconos
            if imagen_seleccionada.endswith(('.jpg', '.png', '.jpeg')) and imagen_seleccionada in os.listdir(iconos_folder):
                
                print(os.path.join(iconos_folder, imagen_seleccionada))
                print(os.listdir(iconos_folder))
                superuser.foto_perfil = os.path.join('iconos/', imagen_seleccionada)
                superuser.save()
                print(superuser.foto_perfil)

                return Response({'exito': 'La imagen seleccionada icono se cargó con éxtio.'}, status=status.HTTP_202_ACCEPTED)
                
            else:
                superuser.foto_perfil = os.path.join('perfil/', imagen_seleccionada)
                superuser.save()
                return Response({'exito': 'La imagen seleccionada perfil se cargó con éxito.'}, status=status.HTTP_202_ACCEPTED)
        else:
        # Si no se especifica ninguna imagen, usa la imagen por defecto
                superuser.foto_perfil = 'perfil/usuario_default.png'

        # Guarda el superusuario
        superuser.save()

        return Response({'valid': True}, status=status.HTTP_200_OK) 
 
class UpdateDatosBasicos(APIView):
    permission_classes = [AllowAny]  
    authentication_classes = [] 
    def post(self, request):

        nombre= request.data.get('nombre')
        apellido= request.data.get('apellido')
        email= request.data.get("email")
    
        
        try:
            user = CustomUser.objects.get(email=email)
            token_exists = Token.objects.filter(user=user).exists()

            if token_exists:

                user.nombre=nombre
                user.apellido=apellido
                user.save()
                print(user)
                return Response({'valid': True}, status=status.HTTP_200_OK) 
            else:
                return Response({'valid': False}, status=status.HTTP_406_NOT_ACCEPTABLE) 

        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class UpdateFotoPerfil(APIView):
    permission_classes = [AllowAny]  
    authentication_classes = [] 
    def post(self, request):
        email = request.data.get('email')
        imagen_seleccionada = request.data.get('imagen_seleccionada')

        try:
            superuser = CustomUser.objects.get(email=email)
            token_exists = Token.objects.filter(user=superuser).exists()
            iconos_folder = os.path.join('media', 'iconos')

            if token_exists:
                if imagen_seleccionada.endswith(('.jpg', '.png', '.jpeg')) and imagen_seleccionada in os.listdir(iconos_folder):
                    superuser.foto_perfil = os.path.join('iconos/', imagen_seleccionada)
                    superuser.save()
                    return Response({'exito': 'La imagen se actualizó con éxito con un icono.'}, status=status.HTTP_202_ACCEPTED)
                else:
                    superuser.foto_perfil = os.path.join('perfil/', imagen_seleccionada)
                    superuser.save()
                    return Response({'exito': 'La imagen seleccionada perfil se actualizó con éxito.'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'exito': 'error'}, status=status.HTTP_404_NOT_FOUND) 

        except CustomUser.DoesNotExist:
            return Response({'exito': 'error'}, status=status.HTTP_404_NOT_FOUND)

class EliminarFotoPerfil(APIView):
    permission_classes = [AllowAny]  
    authentication_classes = [] 
    def post(self, request):
        email = request.data.get('email')
        try:
            superuser = CustomUser.objects.get(email=email)
            token_exists = Token.objects.filter(user=superuser).exists()

            if token_exists:
               superuser.foto_perfil = 'perfil/usuario_default.png'
               superuser.save()
               return Response({'exito': 'La imagen default se actualizó con éxito.'}, status=status.HTTP_200_OK)

            else:
                return Response({'valid': False}, status=status.HTTP_403_FORBIDDEN) 

        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UpdateContraseña(APIView):
    permission_classes = [AllowAny]  
    authentication_classes = [] 
    def post(self, request):
        email= request.data.get('email')
        contrasena= request.data.get('contrasena')
        
        try:
            user = CustomUser.objects.get(email=email)
            token_exists = Token.objects.filter(user=user).exists()
            if contrasena=='' or contrasena==' ':
                return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND) 

            if token_exists:
                user.set_password(contrasena)
                user.save()
                print(contrasena)
                return Response({'valid': True}, status=status.HTTP_200_OK) 
            else:
                # El token no está asociado al usuario
                return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND) 

        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Logout(APIView):
 
    def post(self, request, format=None):
        email = request.data.get('email')

        try:
            user = CustomUser.objects.get(email=email)
            Token.objects.filter(user=user).delete()
            
            return Response({'valid': True}, status=status.HTTP_200_OK) 
        except CustomUser.DoesNotExist:
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND) 
    
