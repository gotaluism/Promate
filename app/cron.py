from django_cron import CronJobBase, Schedule
from .models import Materia
from django.core.mail import send_mail

class MiTareaProgramada(CronJobBase):
    RUN_EVERY_MINS = 5 # cada 5 minutos

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'miapp.mi_tarea_programada' # nombre de la tarea

    def do(self):
        # Obtener el dato de la base de datos
        mi_dato = Materia.objects.get(horarioI=)

        # Verificar si se cumple la condición para enviar la alerta
        if mi_dato.valor > 100:
            # Enviar la alerta por correo electrónico
            send_mail(
                'Alerta de Django',
                'El valor de mi dato es mayor que 100',
                'from@example.com',
                ['to@example.com'],
                fail_silently=False,
            )