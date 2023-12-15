from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Pelicula

admin.site.register(Pelicula)