from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Actor, Genero

admin.site.register(CustomUser)

# Registra los otros modelos
admin.site.register(Actor)
admin.site.register(Genero)
