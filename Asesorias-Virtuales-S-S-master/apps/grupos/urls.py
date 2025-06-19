from django.urls import path
from . import views

app_name = 'grupos'

urlpatterns = [
    path('asesor/', views.grupos_asesor, name='grupos_asesor'),
    path('asesor/programar-reunion/', views.programar_reunion, name='programar_reunion'),
    path('asesor/eliminar/<int:grupo_id>/', views.eliminar_grupo, name='eliminar_grupo'),
    path('asesor/finalizar-asesoria/<int:grupo_id>/', views.finalizar_asesoria, name='finalizar_asesoria'),
] 