from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

from .forms import MateriaForm
from .forms import registrarCarrera, NotaForm
from django.urls import reverse

from datetime import datetime, time, timedelta
from django.core.mail import send_mail
from .models import Materia, User
from tkinter import messagebox as MessageBox
import tkinter as tk
import smtplib
import yagmail
from email.mime.text import MIMEText
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'proyectopromate@gmail.com' # tu dirección de correo electrónico
smtp_password = 'PROMATE12345' # tu contraseña de correo electrónico
yag = yagmail.SMTP("proyectopromate@gmail.com", "xqhcbdivgiilrvfs")
# Create your views here.

def home(request):
    return render(request, 'home.html')

def capturarDatos(request):
    # user = get_object_or_404(User,pk=user_id)
    if request.method == 'GET':
        return render(request, 'captura.html',{'form':registrarCarrera()})
    else:
        try:    
            form = registrarCarrera(request.POST)
            newMateria = form.save(commit=False)
            newMateria.save()
            # return redirect('../actualizarperfil/')
            return render(request,'captura.html',{'mensaje':'Datos Guardados correctamente'})
        except ValueError:
            return render(request,'captura.html',{'form':registrarCarrera(),'error':'bad data passed in'})
    # return render(request, 'captura.html')
    


def calculadora(request):                     
    return render(request, 'calculadora.html')

def calculadora2(request):
    return render(request, 'calculadoracreditos.html')


def calculadora3(request):
    return render(request, 'calculadoraAcumulado.html')


def prueba(request):
    return render(request, 'prueba.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('/login')
            
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'register.html', context)


def login(request):
    return render(request, 'login.html')

def logoutaccount(request):
    logout(request)
    return redirect('home')

def materia(request, user_id):
    user = get_object_or_404(User,pk=user_id)
    materias=Materia.objects.filter(user = user)       
    promedios = {}
    for materia in materias:
        notas = Notas.objects.filter(materia=materia, user=user)
        promedio = 0
        suma_porcentajes = 0
        for nota in notas:
            promedio += nota.nota * nota.porcentaje
            suma_porcentajes += nota.porcentaje
        if suma_porcentajes > 0 and suma_porcentajes <= 100:
            promedioFin = promedio / suma_porcentajes
        elif suma_porcentajes == 0:
            promedioFin = 0.0
        else: 
            promedioFin = "Porcentaje pasa de 100%"
        promedios[materia.id] = promedioFin
        
    mi_instancia = Materia.objects.filter(pk=17).first()
    
    mi_materia = Materia.objects.filter(horarioI__gte=datetime.now(), horarioI__lte=datetime.now() + timedelta(minutes=15)).first()
    if mi_materia:
        #Correo del usuario
        email_address = mi_materia.user.email
        
        yag.send(
            to=email_address,
            subject="Alerta de inicio de clases",
            contents=f'La clase {mi_materia.nombreMateria} está por empezar.',
        ) 
        
    return render(request, 'materias.html', {'materias':materias,'promedios': promedios})

def crearmateria(request, user_id):
    user = get_object_or_404(User,pk=user_id)
    if request.method == 'GET':
        return render(request, 'createmateria.html',{'form':MateriaForm(), 'user':user})
    else:
        try:    
            form = MateriaForm(request.POST)
            newMateria = form.save(commit=False)
            newMateria.user = request.user
            newMateria.user = user
            newMateria.save()
            return redirect('materia/', newMateria.user.id)
        except ValueError:
            return render(request,'createmateria.html',{'form':MateriaForm(),'error':'bad data passed in'})

def actualizarmateria(request,user_id, materia_id):
    materia = get_object_or_404(Materia,pk=materia_id,user=request.user)
    if request.method == 'GET':
        form = MateriaForm(instance=materia)
        return render(request, 'actualizarmateria.html',{'materia': materia,'form':form})
    else:
        try:
            form = MateriaForm(request.POST,instance=materia)
            form.save()
            return redirect('../materia/', materia.user.id)
        except ValueError:
            return render(request,'actualizarmateria.html',{'materia': materia,'form':form,'error':'Bad data in form'})

def eliminarmateria(request,user_id, materia_id):
    materia = get_object_or_404(Materia, pk=materia_id,user=request.user)
    materia.delete()
    return redirect('../materia/', materia.user.id)



def nota(request, user_id, materia_id):                               ###
    user = get_object_or_404(User,pk=user_id)                         ###
    materia = get_object_or_404(Materia,pk=materia_id)    ###
    crear_nota_url = reverse('crearnota', args=[user_id, materia_id])
    notas=Notas.objects.filter(materia = materia,user = user)         ###
    
    
    promedio=0
    suma_porcentajes=0
    for nota in notas:
        promedio+=nota.nota*nota.porcentaje
        suma_porcentajes+=nota.porcentaje
        
    if suma_porcentajes>0 and suma_porcentajes<=100:
        promedioFin=promedio/suma_porcentajes
    elif suma_porcentajes==0:
        promedioFin=0.0
    else: 
        promedioFin= "Porcentaje pasa de 100%"

    
    return render(request, 'notas.html', {'notas':notas , 'crear_nota_url':crear_nota_url, 'promedioFin':promedioFin})             ###

def crearnota(request, user_id, materia_id):
    user = get_object_or_404(User,pk=user_id)
    materia = get_object_or_404(Materia,pk=materia_id)    
    if request.method == 'GET':
        return render(request, 'createnotas.html',{'form':NotaForm(), 'materia':materia})
    else:
        try:
            form = NotaForm(request.POST)
            newNota = form.save(commit=False)
            newNota.user = request.user
            newNota.materia = materia
            newNota.save()
            return redirect('nota',newNota.user.id,newNota.materia.id) ##########33
        except ValueError:
            return render(request,'createnotas.html',{'form':NotaForm(),'error':'bad data passed in'})

def actualizarnota(request,nota_id):
    nota = get_object_or_404(Notas,pk=nota_id,user=request.user)
    if request.method == 'GET':
        form = NotaForm(instance=nota)
        return render(request, 'updatenotas.html',{'nota': nota,'form':form})
    else:
        try:
            form = NotaForm(request.POST,instance=nota)
            form.save()
            return redirect('nota',nota.user.id,nota.materia.id)
        except ValueError:
            return render(request,'updatenotas.html',{'nota': nota,'form':form,'error':'Bad data in form'})

def eliminarnota(request, nota_id):
    nota= get_object_or_404(Notas, pk=nota_id,user=request.user)
    nota.delete()
    return redirect('nota',nota.user.id, nota.materia.id)