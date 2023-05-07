from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Materia)
admin.site.register(Carrera)
admin.site.register(Notas)

admin.site.register(EstadoAnimoAntes)
admin.site.register(EstadoAnimoDespues)