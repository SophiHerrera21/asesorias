from django.urls import path
from . import views

app_name = 'asesorias'

urlpatterns = [
    path('asesor/', views.asesorias_asesor, name='asesorias_asesor'),
    path('asesor/crear/', views.crear_asesoria, name='crear_asesoria'),
    path('asesor/editar/<int:asesoria_id>/', views.editar_asesoria, name='editar_asesoria'),
    path('asesor/detalle/<int:asesoria_id>/', views.detalle_asesoria, name='detalle_asesoria'),
    path('asesor/marcar-realizada/<int:asesoria_id>/', views.marcar_realizada, name='marcar_realizada'),
    path('asesor/reagendar/<int:asesoria_id>/', views.reagendar_asesoria, name='reagendar_asesoria'),
    path('asesor/cancelar/<int:asesoria_id>/', views.cancelar_asesoria, name='cancelar_asesoria'),
] 