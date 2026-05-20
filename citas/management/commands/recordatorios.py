from django.core.management.base import BaseCommand
from django.utils import timezone
from citas.models import Cita
from citas.utils import enviar_recordatorio
from datetime import date, timedelta


class Command(BaseCommand):
    help = "Envía recordatorios de citas para el día siguiente"

    def handle(self, *args, **options):
        manana = date.today() + timedelta(days=1)
        citas = Cita.objects.filter(
            fecha=manana,
            estado__in=['pendiente', 'confirmada']
        ).select_related('paciente', 'dentista')

        for cita in citas:
            enviar_recordatorio(cita)

        self.stdout.write(
            self.style.SUCCESS(f"Recordatorios enviados: {citas.count()} citas para {manana}")
        )