from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

# from .models import Materia
# from .models import Carrera
# from .models import Notas
from .models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label= 'Email')
    password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label = 'Confirm password', widget=forms.PasswordInput)
    
    
    class Meta:
        model = User
        fields =['username', 'email', 'password1', 'password2']

        help_texts = {k:"" for k in fields}
        
class MateriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args,**kwargs)
        self.fields['nombreMateria'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombreProfesor'].widget.attrs.update({'class': 'form-control'})
        self.fields['semestre'].widget.attrs.update({'class': 'form-control', 'input_type': 'number'})
        self.fields['cantCreditos'].widget.attrs.update({'class': 'form-control', 'input_type': 'number'})
        self.fields['horarioI'].widget.attrs.update({'class': 'form-control', 'input_type': 'time'})
        self.fields['horarioF'].widget.attrs.update({'class': 'form-control', 'input_type': 'time'})
        
    class Meta:
        model = Materia
        fields = ['nombreMateria', 'nombreProfesor', 'semestre','cantCreditos', 'horarioI', 'horarioF']
        labels = {
            'nombreMateria': 'Nombre de la materia',
            'semestre': 'Semestre',
            'nombreProfesor': 'Nombre del profesor',
            'cantCreditos': 'Cantidad de créditos',
            'horarioI': 'Horario Inicio',
            'horarioF': 'Horario Finalizacion',
        }
        widgets = {
            'nombreMateria': forms.TextInput(attrs={'class': 'form-control'}),
            'nombreProfesor': forms.TextInput(attrs={'class': 'form-control'}),
            'semestre': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantCreditos': forms.NumberInput(attrs={'class': 'form-control'}),
            'horarioI': forms.TimeInput(attrs={'class': 'form-control'}),
            'horarioF': forms.TimeInput(attrs={'class': 'form-control'}),
        }
        
        
class registrarCarrera(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args,**kwargs)
        self.fields['nombreCarrera'].widget.attrs.update({'class': 'form-control'})
        self.fields['numSemestresTotales'].widget.attrs.update({'class': 'form-control', 'input_type': 'number'})
        self.fields['numTotalCreditos'].widget.attrs.update({'class': 'form-control', 'input_type': 'number'})
    
    class Meta:
        model = Carrera
        fields = ['nombreCarrera', 'numSemestresTotales', 'numTotalCreditos']
        labels = {
            'nombreCarrera': 'Nombre de la carrera',
            'numSemestresTotales': 'Semestres',
            'numTotalCreditos': 'Numero total de creditos'
        }
        widgets = {
            'nombreCarrera': forms.TextInput(attrs={'class': 'form-control'}),
            'numSemestresTotales': forms.TextInput(attrs={'class': 'form-control'}),
            'numTotalCreditos': forms.TextInput(attrs={'class': 'form-control'})
        }

class NotaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args,**kwargs)
        self.fields['nota'].widget.attrs.update({'class': 'form-control' , 'input_type': 'number'})
        self.fields['porcentaje'].widget.attrs.update({'class': 'form-control' , 'input_type': 'number'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})

        
        
    class Meta:
        model = Notas
        fields = ['nota', 'porcentaje','descripcion']
        labels = {
            'nota': 'Nota',
            'porcentaje': 'Porcentaje',
            'descripcion': 'Descripcion'
        }
        widgets = {
            'nota': forms.NumberInput(attrs={'class': 'form-control'}),
            'porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'})
        }
        
class AnimoAntesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args,**kwargs)
        self.fields['estadoAnimoAntes'].widget.attrs.update({'class': 'form-control',})

    class Meta:
        model = EstadoAnimoAntes
        fields = ['estadoAnimoAntes']
        labels = {
            'estadoAnimoAntes': 'Tu estado de animo antes es:'}

class AnimoDespuesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args,**kwargs)
        self.fields['estadoAnimoDespues'].widget.attrs.update({'class': 'form-control',})

    class Meta:
        model = EstadoAnimoDespues
        fields = ['estadoAnimoDespues']
        labels = {
            'estadoAnimoDespues': 'Tu estado de animo despues es:'}
