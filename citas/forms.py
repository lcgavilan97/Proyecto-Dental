from django import forms
from django.core.exceptions import ValidationError
from .models import Dentista, Paciente, Cita, Contacto
from datetime import date, datetime, time
import re

HORARIOS = [
    ("09:00", "09:00"),
    ("09:40", "09:40"),
    ("10:20", "10:20"),
    ("11:00", "11:00"),
    ("11:40", "11:40"),
    ("12:20", "12:20"),
    ("13:00", "13:00"),
    ("13:40", "13:40"),
    ("16:00", "16:00"),
    ("16:40", "16:40"),
    ("17:20", "17:20"),
    ("18:00", "18:00"),
    ("18:40", "18:40"),
]


class ReservaForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        label="Nombre completo",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Juan Pérez"}),
    )
    rut = forms.CharField(
        max_length=12,
        label="RUT",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 12.345.678-9"}),
    )
    telefono = forms.CharField(
        max_length=15,
        label="Teléfono",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: +56 9 1234 5678"}),
    )
    correo = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Ej: juan@correo.cl"}),
    )
    dentista = forms.ModelChoiceField(
        queryset=Dentista.objects.filter(activo=True),
        label="Dentista",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date", "min": date.today().isoformat()}),
    )
    hora = forms.ChoiceField(
        choices=[("", "Selecciona hora")] + HORARIOS,
        label="Hora",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    notas = forms.CharField(
        required=False,
        label="Notas (opcional)",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Comentarios adicionales..."}),
    )

    def clean_rut(self):
        rut = self.cleaned_data["rut"]
        rut_clean = re.sub(r"[^0-9kK]", "", rut)
        if len(rut_clean) < 8:
            raise ValidationError("RUT inválido.")
        return rut

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        if fecha < date.today():
            raise ValidationError("No se pueden agendar citas en el pasado.")
        return fecha

    def clean_hora(self):
        hora_str = self.cleaned_data.get("hora")
        if not hora_str:
            return hora_str
        horas_validas = [h[0] for h in HORARIOS]
        if hora_str not in horas_validas:
            raise ValidationError("Hora no válida.")
        return hora_str

    def clean(self):
        cleaned = super().clean()
        dentista = cleaned.get("dentista")
        fecha = cleaned.get("fecha")
        hora_str = cleaned.get("hora")

        if dentista and fecha and hora_str:
            hora = time.fromisoformat(hora_str)
            existe = Cita.objects.filter(
                dentista=dentista, fecha=fecha, hora=hora
            ).exists()
            if existe:
                raise ValidationError(
                    f"El Dr(a). {dentista.nombre} ya tiene una cita agendada para el {fecha} a las {hora_str}. Por favor elige otro horario."
                )
        return cleaned


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'telefono', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@correo.cl'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Escribe tu mensaje aquí...'}),
        }
        labels = {
            'nombre': 'Nombre completo',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono (opcional)',
            'mensaje': 'Mensaje',
        }