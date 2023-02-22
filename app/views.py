from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'home.html')


def materia(request):
    return render(request, 'materias.html')

def capturarDatos(request):
    return render(request, 'captura.html')

def calculadora(request):
    return render(request, 'calculadora.html')
def calculadora2(request):
    return render(request, 'calculadoracreditos.html')

