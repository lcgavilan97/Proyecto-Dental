from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from simple_history.models import HistoricalRecords


class Dentista(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Dentista"
        verbose_name_plural = "Dentistas"

    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    correo = models.EmailField(unique=True, verbose_name="Correo electrónico")

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"{self.nombre} ({self.rut})"


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, verbose_name="Paciente"
    )
    dentista = models.ForeignKey(
        Dentista, on_delete=models.CASCADE, verbose_name="Dentista"
    )
    fecha = models.DateField(verbose_name="Fecha")
    hora = models.TimeField(verbose_name="Hora")
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name="Estado",
    )
    notas = models.TextField(blank=True, verbose_name="Notas")
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Creada")
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name="Actualizada")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        unique_together = ['dentista', 'fecha', 'hora']

    def __str__(self):
        return f"{self.paciente} - {self.dentista} - {self.fecha} {self.hora}"

    def clean(self):
        if self.fecha and self.fecha < date.today():
            raise ValidationError("No se pueden agendar citas en el pasado.")


class Testimonio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    contenido = models.TextField(verbose_name="Testimonio")
    rating = models.PositiveSmallIntegerField(
        default=5,
        choices=[(i, f"{i} estrella{'s' if i > 1 else ''}") for i in range(1, 6)],
        verbose_name="Calificación"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")

    class Meta:
        verbose_name = "Testimonio"
        verbose_name_plural = "Testimonios"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre} - {self.rating}/5"


class Galeria(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    imagen = models.ImageField(upload_to='galeria/', verbose_name="Imagen")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Imagen de galería"
        verbose_name_plural = "Galería de imágenes"
        ordering = ['orden']

    def __str__(self):
        return self.titulo


class Contacto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=15, blank=True, verbose_name="Teléfono")
    mensaje = models.TextField(verbose_name="Mensaje")
    leido = models.BooleanField(default=False, verbose_name="Leído")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviado")

    class Meta:
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre} - {self.mensaje[:50]}"