from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'home.html')


def materia(request):
    return render(request, 'materias.html')

def capturarDatos(request):
    return render(request, 'captura.html')

