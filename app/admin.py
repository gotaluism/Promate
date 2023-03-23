from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Estudiante)
admin.site.register(Materia)
admin.site.register(Carrera)
admin.site.register(Notas)