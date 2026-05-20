from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportMixin
from import_export import resources
from .models import Dentista, Paciente, Cita, Testimonio, Galeria, Contacto


# ─── Dentista ────────────────────────────────────────────────

@admin.register(Dentista)
class DentistaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especialidad', 'activo')
    list_filter = ('especialidad', 'activo')
    search_fields = ('nombre',)


# ─── Paciente ────────────────────────────────────────────────

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'telefono', 'correo')
    search_fields = ('nombre', 'rut', 'correo')


# ─── Cita ────────────────────────────────────────────────────

class CitaResource(resources.ModelResource):
    class Meta:
        model = Cita
        fields = ['id', 'paciente__nombre', 'paciente__rut', 'dentista__nombre',
                   'fecha', 'hora', 'estado', 'notas', 'created_at']
        export_order = fields


@admin.register(Cita)
class CitaAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = CitaResource
    list_display = ('paciente', 'dentista', 'fecha', 'hora', 'estado_coloreado', 'created_at')
    list_filter = ('estado', 'fecha', 'dentista')
    search_fields = ('paciente__nombre', 'paciente__rut', 'dentista__nombre')
    date_hierarchy = 'fecha'
    ordering = ('-fecha', '-hora')
    actions = ['confirmar_citas', 'cancelar_citas']

    def estado_coloreado(self, obj):
        colores = {'pendiente': 'warning', 'confirmada': 'success', 'cancelada': 'danger'}
        return format_html(
            '<span class="badge bg-{}" style="cursor:pointer" onclick="window.location.href=\'{}/{}/change/\'">{}</span>',
            colores.get(obj.estado, 'secondary'),
            obj._meta.app_label, obj.pk, obj.get_estado_display()
        )
    estado_coloreado.short_description = 'Estado'

    def confirmar_citas(self, request, queryset):
        queryset.update(estado='confirmada')
    confirmar_citas.short_description = 'Confirmar citas seleccionadas'

    def cancelar_citas(self, request, queryset):
        queryset.update(estado='cancelada')
    cancelar_citas.short_description = 'Cancelar citas seleccionadas'


# ─── Testimonio ──────────────────────────────────────────────

@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rating', 'activo', 'created_at')
    list_filter = ('activo', 'rating')
    search_fields = ('nombre', 'contenido')


# ─── Galeria ─────────────────────────────────────────────────

@admin.register(Galeria)
class GaleriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'orden', 'activo', 'vista_previa')
    list_filter = ('activo',)
    search_fields = ('titulo',)

    def vista_previa(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="height: 50px; border-radius: 6px;">', obj.imagen.url)
        return '-'
    vista_previa.short_description = 'Vista previa'


# ─── Contacto ─────────────────────────────────────────────────

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'leido', 'created_at', 'mensaje_corto')
    list_filter = ('leido', 'created_at')
    search_fields = ('nombre', 'email', 'mensaje')
    actions = ['marcar_como_leido']

    def mensaje_corto(self, obj):
        return obj.mensaje[:60] + ('...' if len(obj.mensaje) > 60 else '')
    mensaje_corto.short_description = 'Mensaje'

    def marcar_como_leido(self, request, queryset):
        queryset.update(leido=True)
    marcar_como_leido.short_description = 'Marcar como leídos'