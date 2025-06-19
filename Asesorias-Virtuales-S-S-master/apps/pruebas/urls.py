from django.urls import path
from . import views

app_name = 'pruebas'

urlpatterns = [
    path('asesor/', views.pruebas_asesor, name='pruebas_asesor'),
    path('asesor/crear/', views.crear_prueba, name='crear_prueba'),
    path('asesor/entregas/<int:prueba_id>/', views.entregas_prueba, name='entregas_prueba'),
    path('asesor/eliminar/<int:prueba_id>/', views.eliminar_prueba, name='eliminar_prueba'),
] 