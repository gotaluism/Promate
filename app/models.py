from django.db import models
from django.contrib.auth.models import User 
from datetime import time
# Create your models here.




    
class Materia(models.Model):
    nombreMateria = models.CharField(max_length=50)
    semestre=models.IntegerField()
    nombreProfesor=models.CharField(max_length=50)
    cantCreditos=models.IntegerField()
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    horarioI = models.TimeField(default=time(9,0,0))
    horarioF = models.TimeField(default=time(12,0,0))
    estadoAnimoAntes = models.CharField(max_length=500)
    estadoAnimoDespues = models.CharField(max_length=500)
    
class Carrera(models.Model):
    nombreCarrera = models.CharField(max_length=50)
    numSemestresTotales = models.IntegerField()
    numTotalCreditos = models.IntegerField()
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    

class Notas(models.Model):
    nota = models.FloatField()
    porcentaje=models.IntegerField()
    descripcion=models.CharField(max_length=50)
    
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia,on_delete=models.CASCADE)
    
    def __str__(self):
        return "{}-{}".format(self.nota,self.descripcion)
    
