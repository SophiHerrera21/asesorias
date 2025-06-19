from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('asesor/', views.notificaciones_asesor, name='notificaciones_asesor'),
] 