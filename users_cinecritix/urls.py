from django.urls import path, include
from .views import UsuariosList
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from .views import LoginView
from .views import RegisterUserView
from .views import Logout
from .views import UpdateContraseña
from rest_framework.documentation import include_docs_urls

router= routers.DefaultRouter()
 #Aplicacion o clase desde donde, vista, nombre
router.register('listaUser', UsuariosList, 'usuarioList1' )

urlpatterns = [
    path('usuario/', include(router.urls)),
    path('docs/', include_docs_urls(title="modulo API")),
    path('login/', LoginView.as_view(), name='login_view'),
    path('register/', RegisterUserView.as_view(), name="register"),
    path('update_contra/', UpdateContraseña.as_view(), name='update_contra'),
    path('logout/', Logout.as_view(), name='logout'),
]