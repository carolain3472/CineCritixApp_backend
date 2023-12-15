from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Serie

admin.site.register(Serie)