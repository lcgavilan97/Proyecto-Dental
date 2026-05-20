from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Dentista, Paciente, Cita
from .serializers import (
    DentistaSerializer, PacienteSerializer, CitaSerializer, CitaAdminSerializer
)


class DentistaViewSet(viewsets.ModelViewSet):
    queryset = Dentista.objects.filter(activo=True)
    serializer_class = DentistaSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all().select_related('paciente', 'dentista')
    serializer_class = CitaSerializer

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return CitaAdminSerializer
        return CitaSerializer


@api_view(['GET'])
def disponibilidad(request, dentista_id):
    from datetime import date, time
    fecha_str = request.GET.get('fecha')

    if not fecha_str:
        return Response(
            {"error": "Parámetro 'fecha' es requerido (YYYY-MM-DD)."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        fecha = date.fromisoformat(fecha_str)
    except ValueError:
        return Response(
            {"error": "Formato de fecha inválido. Use YYYY-MM-DD."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if fecha < date.today():
        return Response(
            {"horarios": []}
        )

    HORARIOS = [
        "09:00", "09:40", "10:20", "11:00", "11:40", "12:20", "13:00", "13:40",
        "16:00", "16:40", "17:20", "18:00", "18:40",
    ]

    ocupado = set(
        Cita.objects.filter(dentista_id=dentista_id, fecha=fecha)
        .values_list('hora', flat=True)
    )

    disponibles = [
        {"hora": h, "disponible": True} for h in HORARIOS
        if time.fromisoformat(h) not in ocupado
    ]

    return Response({"fecha": fecha_str, "horarios": disponibles})


@api_view(['GET'])
def salud(self):
    return Response({"status": "ok", "service": "Nuba Dental API"})