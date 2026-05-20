from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Cita


def enviar_confirmacion(cita):
    asunto = f"Confirmacion de Cita - Nuba Dental"
    mensaje = render_to_string('emails/confirmacion_cita.html', {
        'cita': cita,
        'site_url': 'http://127.0.0.1:8080',
    })
    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [cita.paciente.correo],
        html_message=mensaje,
        fail_silently=True,
    )


def enviar_recordatorio(cita):
    asunto = f"Recordatorio de Cita - Nuba Dental"
    mensaje = render_to_string('emails/recordatorio_cita.html', {
        'cita': cita,
        'site_url': 'http://127.0.0.1:8080',
    })
    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [cita.paciente.correo],
        html_message=mensaje,
        fail_silently=True,
    )