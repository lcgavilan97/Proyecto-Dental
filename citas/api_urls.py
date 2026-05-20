from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'dentistas', api_views.DentistaViewSet)
router.register(r'pacientes', api_views.PacienteViewSet)
router.register(r'citas', api_views.CitaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('disponibilidad/<int:dentista_id>/', api_views.disponibilidad, name='disponibilidad'),
    path('salud/', api_views.salud, name='salud'),
]