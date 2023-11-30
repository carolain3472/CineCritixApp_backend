from django.urls import path, include, re_path
from django.conf.urls.static import static
from cinecritix_backend import settings
from .views import DatosUsuarioObtener, UsuariosList, validar_token
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from .views import LoginView
from .views import RegisterUserView
from .views import Logout
from .views import UpdateContraseña, Saludo, UpdateDatosBasicos, DarmeDeBaja, EliminarFotoPerfil,UserProfileView,UpdateFotoPerfil,EstablecerIcono
from rest_framework.documentation import include_docs_urls
from django.conf import Settings
from django.views.static import serve


router= routers.DefaultRouter()
 #Aplicacion o clase desde donde, vista, nombre
router.register('listaUser', UsuariosList, 'usuarioList1' )

urlpatterns = [
    path('usuario/', include(router.urls)),
    path('docs/', include_docs_urls(title="modulo API")),
    path('login/', LoginView.as_view(), name='login_view'),
    path('register/', RegisterUserView.as_view(), name="register"),
    path('update_contra/', UpdateContraseña.as_view(), name='update_contra'),
    path('update-datos-basicos/', UpdateDatosBasicos.as_view(), name='update_datos_basicos'),
    path('update-profile/', UpdateFotoPerfil.as_view(), name="update_profile"),
    path('quitar-profile/', EliminarFotoPerfil.as_view(), name="quitar_profile"),
    path('logout/', Logout.as_view(), name='logout'),
    path('darme-de-baja/', DarmeDeBaja.as_view(), name='darme_de_baja'),
    path('saludo/', Saludo.as_view(), name='saludo'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path("validate_token/", validar_token.as_view(), name="token-validate"),
    path("obtener-informacion/", DatosUsuarioObtener.as_view(), name="obtener_informacion"),
    path("enviar-icono/", EstablecerIcono.as_view(), name="establecer_icono"),

    

    
    
    


]
