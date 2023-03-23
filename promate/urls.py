from django.contrib import admin
from django.urls import path

from app import views as appViews
from django.contrib.auth.views import LoginView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', appViews.home, name='home'),
    path('login/captura/', appViews.capturarDatos, name='captura'),
    path('calculadora/', appViews.calculadora, name='calculadora'),
    path('calculadora2/', appViews.calculadora2, name='calculadora2'),
    path('calculadora3/', appViews.calculadora3, name='calculadora3'),
    path('prueba/', appViews.prueba, name='prueba'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('registro/', appViews.register, name='register'),
    path('logout/', appViews.logoutaccount, name='logoutaccount'),
    
    path('usuario/<int:user_id>/materia/', appViews.materia, name='materia'),
    path('usuario/<int:user_id>/crearmateria' , appViews.crearmateria, name='crearmateria'),
    path('usuario/<int:user_id>/actualizarmateria/<int:materia_id>' , appViews.actualizarmateria, name='actualizarmateria'),
    path('usuario/<int:user_id>/eliminarmateria/<int:materia_id>' , appViews.eliminarmateria, name='eliminarmateria'),
    
    path('usuario/<int:user_id>/materia/<int:materia_id>/nota' , appViews.nota, name='nota'),##############
    path('usuario/<int:user_id>/materia/<int:materia_id>/crearnota' , appViews.crearnota, name='crearnota'),
    path('usuario/<int:user_id>/materia/<int:materia_id>/actualizarnota/<int:nota_id>' , appViews.actualizarnota, name='actualizarnota'),
    path('usuario/<int:user_id>/materia/<int:materia_id>/eliminarnota/<int:nota_id>' , appViews.actualizarnota, name='eliminarnota'),
]
