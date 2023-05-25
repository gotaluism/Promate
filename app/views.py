from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.views.generic import TemplateView


from .forms import *

from django.urls import reverse

from datetime import datetime,  timedelta

from .models import Materia, User



import yagmail

smtp_server = 'smtp.gmail.com'
smtp_port = 587

yag =  yagmail.SMTP("promatepi2@gmail.com", "rjqrxpnhpgavlgvk")
# Create your views here.

def home(request):
    return render(request, 'home.html')

def aggperfil(request, user_id):
    user = get_object_or_404(User,pk=user_id)
    carreras=Carrera.objects.filter(user = user)
    if carreras.count()>=2:
        return render(request,'captura.html',{'form':"-",'error':'Ya hay 2 carreras registradas'})
    else:
        if request.method == 'GET':
            return render(request, 'captura.html',{'form':registrarCarrera(),'user':user})
        else:
            try:    
                form = registrarCarrera(request.POST)
                newMateria = form.save(commit=False)
                newMateria.user=request.user
                newMateria.save()
                return redirect('perfil',newMateria.user.id)
                #return render(request,'captura.html',{'mensaje':'Datos Guardados correctamente'})
            except ValueError:
                return render(request,'captura.html',{'form':registrarCarrera(),'error':'bad data passed in'})
    # return render(request, 'captura.html')
    
def perfil(request,user_id):
    user = get_object_or_404(User,pk=user_id)
    carreras=Carrera.objects.filter(user = user)
    return render(request,'perfil.html',{'carreras':carreras})

def delperfil(request,user_id,carrera_id):
    carrera = get_object_or_404(Carrera, pk=carrera_id,user=request.user)
    carrera.delete()
    return redirect('perfil',carrera.user.id)

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

#___MATERIA___________________________________________________________________
@login_required
def materia(request, user_id):
    user = get_object_or_404(User,pk=user_id)
    searchTerm = request.GET.get('filtroSemestre')
    labels=[]
    data=[]
    notaMateriasIncompleto=0
    creditosVistos=0
    GPA=0
    
    if searchTerm:
        semestres = searchTerm.split(",") 
        materias=Materia.objects.filter(user = user,semestre__in=semestres)
    else:
        materias=Materia.objects.filter(user = user)
        searchTerm="-"
        
    promedios = {}
    for materia in materias:
        notas = Notas.objects.filter(materia=materia, user=user)
        promedio = 0
        suma_porcentajes = 0
        for nota in notas:
            promedio += nota.nota * nota.porcentaje
            suma_porcentajes += nota.porcentaje
        if suma_porcentajes > 0 and suma_porcentajes <= 100:
            promedioFin = round((promedio/suma_porcentajes),2)
        else: 
            promedioFin = 0.0
        promedios[materia.id] = promedioFin
        materia.promedio = promedioFin
        
        notaMateriasIncompleto=notaMateriasIncompleto+(promedioFin*materia.cantCreditos)
        creditosVistos=creditosVistos+materia.cantCreditos
        
        if(notaMateriasIncompleto == 0 and creditosVistos ):
            GPA=0
        else: 
            GPA=round((notaMateriasIncompleto/creditosVistos),2)
        
        labels.append(materia.nombreMateria)
        data.append(promedioFin)
    
    
    mi_materia = Materia.objects.filter(horarioI__gte=datetime.now(), horarioI__lte=datetime.now() + timedelta(minutes=15)).first()
    # if mi_materia:
    #     #Correo del usuario
    #     email_address = mi_materia.user.email
        
    #     yag.send(
    #         to=email_address,
    #         subject="Alerta de inicio de clases",
    #         contents=f'La clase {mi_materia.nombreMateria} está por empezar, entra a Promate e introduce como te sientes!!',
    #     )
        # return redirect('aggestadoanimoantes', mi_materia.user.id ,mi_materia.id )
        
    return render(request, 'materias.html', {'materias':materias,'promedios': promedios,'labels':labels,'data':data,'searchTerm':searchTerm,'GPA':GPA})

#diccionario, 
@login_required
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

@login_required
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

@login_required
def eliminarmateria(request,user_id, materia_id):
    materia = get_object_or_404(Materia, pk=materia_id,user=request.user)
    materia.delete()
    return redirect('../materia/', materia.user.id)
#______________________________________________________________________

#____NOTAA______________________________________________________________________
@login_required
def nota(request, user_id, materia_id): 

    labels=[]
    data=[]
    
    labels1=["FELIZ","TRISTE","ESTRESADO","ABURRIDO"]

    
    
    
    user = get_object_or_404(User,pk=user_id)                         ###
    materia = get_object_or_404(Materia,pk=materia_id)    ###
    crear_nota_url = reverse('crearnota', args=[user_id, materia_id])
    crear_animo_antes= 0
    crear_animo_despues= 0 
    notas=Notas.objects.filter(materia = materia,user = user)
    materias=Materia.objects.filter(user=user)   
    mood=EstadoAnimoAntes.objects.filter(materia = materia,user = user)
    mooder=EstadoAnimoDespues.objects.filter(materia = materia,user = user)
    print(materia.horarioI)

#---------------------------------------------------------------------___________________________
    mi_materia_antes = Materia.objects.filter(user=user,horarioI__gte=datetime.now(), horarioI__lte=datetime.now() + timedelta(minutes=15)).first()
    mi_materia_despues = Materia.objects.filter(user=user,horarioF__gte=datetime.now()- timedelta(minutes=15) , horarioF__lte=datetime.now()).first()
    
    if mi_materia_antes:
        crear_animo_antes= reverse('aggestadoanimoantes', args=[user_id, mi_materia_antes.id])
    
    if mi_materia_despues:
        crear_animo_despues= reverse('aggestadoanimodespues', args=[user_id, mi_materia_despues.id])
#---------------------------------------------------------------------______________________---
    feliz=0
    triste=0
    aburrido=0
    estresado=0
    
    feliz1=0
    triste1=0
    aburrido1=0
    estresado1=0
    
    for notica in notas:
        labels.append(notica.descripcion)
        data.append(notica.nota)
        
    for moodsito in mood:
        if moodsito.estadoAnimoAntes==1:
            feliz=feliz+1
        elif moodsito.estadoAnimoAntes==2:
            triste=triste+1
        elif moodsito.estadoAnimoAntes==3:
            estresado=estresado+1
        else:
            aburrido=aburrido+1
            
            
    for moodsit in mooder:
        if moodsit.estadoAnimoDespues==1:
            feliz1=feliz1+1
        elif moodsit.estadoAnimoDespues==2:
            triste1=triste1+1
        elif moodsit.estadoAnimoDespues==3:
            estresado1=estresado1+1
        else:
            aburrido1=aburrido1+1
            
    data1=[feliz,triste,estresado,aburrido]  
    data2=[feliz1,triste1,estresado1,aburrido1]  
    promedio=0
    suma_porcentajes=0
    for nota in notas:
        promedio+=nota.nota*nota.porcentaje
        suma_porcentajes+=nota.porcentaje
        
    if suma_porcentajes>0 and suma_porcentajes<=100:
        promedioFin=round((promedio/suma_porcentajes),2)
    else:
        promedioFin=0.0
    promediomood=0
    for moods in mood:
        promediomood=int((promediomood+moods.estadoAnimoAntes)/2)
        

    return render(request, 'notas.html', {'notas':notas ,'materias':materias, 'crear_nota_url':crear_nota_url, 'mi_materia_antes':mi_materia_antes,'mi_materia_despues':mi_materia_despues,'crear_animo_antes':crear_animo_antes,'crear_animo_despues':crear_animo_despues,'promedioFin':promedioFin,'sumaPorcentajes':suma_porcentajes,'labels':labels,'data':data,'labels1':labels1,'data1':data1,'promediomood':promediomood,'data2':data2, })             ###

@login_required
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

@login_required
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

@login_required
def eliminarnota(request, nota_id):
    nota= get_object_or_404(Notas, pk=nota_id,user=request.user)
    nota.delete()
    return redirect('nota',nota.user.id, nota.materia.id)
#_______________________________________________________________________________

#___ESTADO ANIMO ANTES________________________________________________________________
def aggestadoanimoantes(request, user_id, materia_id):
    user = get_object_or_404(User,pk=user_id)
    materia = get_object_or_404(Materia,pk=materia_id)  
    mood=EstadoAnimoAntes.objects.filter(materia = materia,user = user)
    promediomood=0
    for moods in mood:
        promediomood=int((promediomood+moods.estadoAnimoAntes)/2)
    if request.method == 'GET':
        return render(request, 'createAnimoAntes.html',{'form':AnimoAntesForm(), 'materia':materia,'promediomood':promediomood})
    else:
        try:
            form = AnimoAntesForm(request.POST)
            newNota = form.save(commit=False)
            newNota.user = request.user
            newNota.materia = materia
            newNota.save()
            return redirect('nota',newNota.user.id,newNota.materia.id) ##########33
        except ValueError:
            return render(request,'createAnimoAntes.html',{'form':AnimoAntesForm(),'error':'bad data passed in'})

#______________________________________________________________________

#___ESTADO ANIMO DESPUES___________________________________________________________________
def aggestadoanimodespues(request, user_id, materia_id):
    user = get_object_or_404(User,pk=user_id)
    materia = get_object_or_404(Materia,pk=materia_id)  
    if request.method == 'GET':
        return render(request, 'createAnimoDespues.html',{'form':AnimoDespuesForm(), 'materia':materia})
    else:
        try:
            form = AnimoDespuesForm(request.POST)
            newNota = form.save(commit=False)
            newNota.user = request.user
            newNota.materia = materia
            newNota.save()
            return redirect('nota',newNota.user.id,newNota.materia.id) ##########33
        except ValueError:
            return render(request,'createAnimoDespues.html',{'form':AnimoDespuesForm(),'error':'bad data passed in'})
#______________________________________________________________________
class chart(TemplateView):
    template_name="notas.html"
    def get_context_data(self,**kwargs):
        context=super().get_context_data(self, **kwargs)    
        context = super().get_context_data(**kwargs)
        context["qs"] = Notas.objects.all()
        return context
    


