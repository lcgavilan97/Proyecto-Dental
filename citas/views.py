from django.shortcuts import redirect, get_object_or_404
from django.views.generic import FormView, ListView, TemplateView, View
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import JsonResponse
from .models import Dentista, Paciente, Cita, Testimonio, Galeria, Contacto
from .forms import ReservaForm, ContactoForm
from .utils import enviar_confirmacion
from datetime import date, timedelta
import re


class LandingPageView(TemplateView):
    template_name = "citas/landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dentistas"] = Dentista.objects.filter(activo=True)
        context["testimonios"] = Testimonio.objects.filter(activo=True)[:6]
        context["galeria"] = Galeria.objects.filter(activo=True)[:8]
        return context


class ReservaView(FormView):
    form_class = ReservaForm
    template_name = "citas/reserva.html"
    success_url = reverse_lazy("reserva_exitosa")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dentistas"] = Dentista.objects.filter(activo=True)
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        rut_clean = re.sub(r"[^0-9kK]", "", data["rut"]).upper()

        paciente, _ = Paciente.objects.update_or_create(
            rut__iexact=rut_clean,
            defaults={
                "nombre": data["nombre"],
                "rut": rut_clean,
                "telefono": data["telefono"],
                "correo": data["correo"],
            },
        )

        from datetime import time
        hora = time.fromisoformat(data["hora"])

        cita = Cita.objects.create(
            paciente=paciente,
            dentista=data["dentista"],
            fecha=data["fecha"],
            hora=hora,
            notas=data["notas"],
        )

        enviar_confirmacion(cita)
        messages.success(self.request, "Tu cita ha sido agendada exitosamente. Revisa tu correo.")
        return redirect(self.success_url)


class ReservaExitosaView(TemplateView):
    template_name = "citas/reserva_exitosa.html"


class MisCitasView(ListView):
    model = Cita
    template_name = "citas/mis_citas.html"
    context_object_name = "citas"

    def get_queryset(self):
        rut = self.request.GET.get("rut")
        if rut:
            return Cita.objects.filter(
                paciente__rut=rut
            ).select_related("paciente", "dentista").order_by("fecha", "hora")
        return Cita.objects.none()


class CancelarCitaView(View):
    def post(self, request, cita_id):
        cita = get_object_or_404(Cita, id=cita_id)
        cita.estado = "cancelada"
        cita.save()
        messages.success(request, "Tu cita ha sido cancelada exitosamente.")
        rut = request.POST.get("rut", "")
        return redirect(f"{reverse('mis_citas')}?rut={rut}")


class ContactoView(FormView):
    form_class = ContactoForm
    template_name = "citas/contacto.html"
    success_url = reverse_lazy("contacto_exitoso")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Mensaje enviado. Te responderemos pronto.")
        return redirect(self.success_url)


class ContactoExitosaView(TemplateView):
    template_name = "citas/contacto_exitoso.html"


class CalendarioView(TemplateView):
    template_name = "citas/calendario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rut = self.request.GET.get("rut", "")

        hoy = date.today()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        semanas = []

        for s in range(4):
            semana = []
            for d in range(7):
                dia = inicio_semana + timedelta(weeks=s, days=d)
                qs = Cita.objects.filter(fecha=dia).select_related('dentista', 'paciente').order_by('hora')
                if rut:
                    qs = qs.filter(paciente__rut=rut)
                semana.append({
                    'fecha': dia,
                    'citas': qs,
                    'hoy': dia == hoy,
                    'mes_actual': dia.month == hoy.month,
                })
            semanas.append(semana)
        context['semanas'] = semanas
        context['mes'] = hoy.strftime('%B %Y').capitalize()
        context['rut'] = rut
        return context