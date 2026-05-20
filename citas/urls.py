from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),
    path('reserva/', views.ReservaView.as_view(), name='reserva'),
    path('reserva/exitosa/', views.ReservaExitosaView.as_view(), name='reserva_exitosa'),
    path('mis-citas/', views.MisCitasView.as_view(), name='mis_citas'),
    path('mis-citas/<int:cita_id>/cancelar/', views.CancelarCitaView.as_view(), name='cancelar_cita'),
    path('contacto/', views.ContactoView.as_view(), name='contacto'),
    path('contacto/exitoso/', views.ContactoExitosaView.as_view(), name='contacto_exitoso'),
    path('calendario/', views.CalendarioView.as_view(), name='calendario'),
]