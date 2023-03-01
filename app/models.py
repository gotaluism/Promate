from django.db import models
# Create your models here.

class Estudiante(models.Model):
    idEstudiante = models.CharField(primary_key=True,max_length=15)
    nombre = models.CharField(max_length=50)
    
    

