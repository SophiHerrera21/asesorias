from django.urls import path
from . import views

app_name = 'pqrs'

urlpatterns = [
    path('asesor/', views.pqrs_asesor, name='pqrs_asesor'),
    path('asesor/responder/<int:pqrs_id>/', views.responder_pqrs, name='responder_pqrs'),
    path('aprendiz/', views.pqrs_aprendiz, name='pqrs_aprendiz'),
    path('aprendiz/<int:pqrs_id>/', views.detalle_pqrs, name='detalle_pqrs'),
    path('coordinador/', views.pqrs_coordinador, name='pqrs_coordinador'),
    path('coordinador/responder/<int:pqrs_id>/', views.responder_pqrs, name='responder_pqrs'),
    path('coordinador/cambiar-estado/<int:pqrs_id>/', views.cambiar_estado_pqrs, name='cambiar_estado_pqrs'),
    path('coordinador/exportar-excel/', views.exportar_excel, name='exportar_excel'),
] 