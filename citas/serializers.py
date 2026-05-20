from rest_framework import serializers
from .models import Dentista, Paciente, Cita
from datetime import date


class DentistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dentista
        fields = ['id', 'nombre', 'especialidad', 'activo']


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id', 'nombre', 'rut', 'telefono', 'correo']
        extra_kwargs = {
            'rut': {'validators': []},
            'correo': {'validators': []},
        }


class CitaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.CharField(source='paciente.nombre', read_only=True)
    dentista_nombre = serializers.CharField(source='dentista.nombre', read_only=True)
    paciente_rut = serializers.CharField(source='paciente.rut', read_only=True)

    class Meta:
        model = Cita
        fields = [
            'id', 'paciente', 'paciente_nombre', 'paciente_rut',
            'dentista', 'dentista_nombre', 'fecha', 'hora', 'estado', 'notas'
        ]
        read_only_fields = ['estado']

    def validate(self, attrs):
        if attrs.get('fecha') and attrs['fecha'] < date.today():
            raise serializers.ValidationError({"fecha": "No se pueden agendar citas en el pasado."})
        return attrs

    def validate(self, attrs):
        dentista = attrs.get('dentista')
        fecha = attrs.get('fecha')
        hora = attrs.get('hora')
        if dentista and fecha and hora:
            conflicto = Cita.objects.filter(
                dentista=dentista, fecha=fecha, hora=hora
            ).exclude(
                pk=self.instance.pk if self.instance else None
            ).exists()
            if conflicto:
                raise serializers.ValidationError(
                    {"hora": "Este horario ya está ocupado con otro paciente."}
                )
        return super().validate(attrs)


class CitaAdminSerializer(CitaSerializer):
    class Meta(CitaSerializer.Meta):
        fields = CitaSerializer.Meta.fields + ['created_at', 'updated_at']
        read_only_fields = ['estado', 'created_at', 'updated_at']