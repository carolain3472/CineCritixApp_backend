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
from .models import CustomUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UsuariosList(viewsets.ModelViewSet):
    """
    Esta vista permite listar usuarios según varios filtros proporcionados en la solicitud POST.
    Atributos:
        None
    Métodos:
        - post: Maneja la solicitud POST para listar usuarios con filtros personalizados.
    """

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

                # Crear una lista de filtros a aplicar
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

    """
    Esta vista permite a los usuarios autenticarse en la aplicación.
    Atributos:
        - template_name: Nombre del archivo de plantilla HTML para la página de inicio de sesión.
        - form_class: Clase de formulario para la autenticación del usuario.
        - success_url: URL a la que se redirige al usuario después de iniciar sesión con éxito.
    Métodos:
        - dispatch: Maneja la solicitud y redirige a la página principal si el usuario ya está autenticado.
        - form_valid: Maneja la validación del formulario de inicio de sesión y la autenticación del usuario.
    """
        
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
        
class LoginView(APIView):

    permission_classes = [AllowAny]  
    authentication_classes = [] 
        
    """
    Esta vista permite a los usuarios autenticarse mediante una solicitud POST a través de API.
    Atributos:
        None
    Métodos:
        - post: Maneja la solicitud POST para autenticar a los usuarios y proporcionar un token de autenticación.
    """
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('contrasena')

        try:
            # Buscar al usuario por cédula en la base de datos
            usuario = CustomUser.objects.get(email=email)
            print(usuario)
            print(password)

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
                                     'user_email': user.email,

                                     })

                

        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Las credenciales proporcionadas son inválidas.')
        
        print("No existe el usuario o contra incorrecta")

        return Response({'valid': False})



class Saludo(APIView):
    def post(self, request):
        nombre = request.data.get('nombre')
        print(nombre)
        return Response({"mensaje": f"Hola, {nombre}!"}, status=status.HTTP_200_OK)
    
class RegisterUserView(APIView):
        
    """
    Esta vista permite registrar nuevos usuarios en la aplicación.
    Atributos:
        - permission_classes: Lista de permisos para permitir el acceso sin autenticación.
        - authentication_classes: Lista de clases de autenticación (ninguna en este caso).
    Métodos:
        - post: Maneja la solicitud POST para registrar un nuevo usuario.
    """
    permission_classes = [AllowAny]  
    authentication_classes = []  

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        nombre= request.data.get('nombre')
        documento= request.data.get("documento")
        email= request.data.get('email')
        contrasena= request.data.get('contrasena')

        try:
            try:
                validate_email(email)
            except ValidationError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
                 

            superuser = CustomUser.objects.create_superuser(
                    nombre=nombre,
                    documento=documento,
                    email=email,
                    password=contrasena
        )
        
                #user = CustomUser.objects.create_superuser(**serializer.validated_data)
            superuser.is_staff = True
            superuser.is_superuser = True
         
            return Response({'valid': True}, status=status.HTTP_200_OK)
        except:
             return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
 
class UpdateContraseña(APIView):
    """
    Esta vista permite a los usuarios actualizar su contraseña.
    Atributos:
        None
    Métodos:
        - post: Maneja la solicitud POST para actualizar la contraseña de un usuario.
    """

    def post(self, request):
        email= request.data.get('email')
        password= request.data.get('password')
        
        try:
            # Buscar al usuario por nombre de usuario en la base de datos
            user = CustomUser.objects.get(email=email)

            token_exists = Token.objects.filter(user=user).exists()

            if password=='' or password==' ':
                return Response(status=status.HTTP_400_BAD_REQUEST)


            if token_exists:
                user.set_password(password)
                user.save()
                print(password)
                return Response(status=status.HTTP_200_OK)
            else:
                # El token no está asociado al usuario
                return Response(status=status.HTTP_404_NOT_FOUND)

        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Logout(APIView):

    """
    Esta vista permite a los usuarios cerrar sesión y eliminar su token de autenticación.
    Atributos:
        None
    Métodos:
        - post: Maneja la solicitud POST para realizar el logout y eliminar el token de acceso.
    """
        
    def post(self, request, format=None):
        email = request.data.get('email')

        try:
            # Buscar al usuario por nombre de usuario en la base de datos
            user = CustomUser.objects.get(email=email)
            
            # Eliminar el token de acceso del usuario
            Token.objects.filter(user=user).delete()
            
            return Response(status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    