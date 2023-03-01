from django.contrib import admin
from django.urls import path

from app import views as appViews
from django.contrib.auth.views import LoginView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', appViews.home, name='home'),
    path('login/captura/', appViews.capturarDatos, name='captura'),
    path('materia/', appViews.materia, name='materia'),
    path('calculadora/', appViews.calculadora, name='calculadora'),
    path('calculadora2/', appViews.calculadora2, name='calculadora2'),
    path('prueba/', appViews.prueba, name='prueba'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('registro/', appViews.register, name='register'),
]
