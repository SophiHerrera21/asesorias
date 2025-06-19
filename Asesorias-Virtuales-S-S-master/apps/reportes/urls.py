from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    # path('asesor/', views.reportes_asesor, name='reportes_asesor'),
    # path('asesor/exportar-excel/', views.exportar_excel_asesor, name='exportar_excel_asesor'),
    path('coordinador/', views.reportes_coordinador, name='reportes_coordinador'),
    path('coordinador/exportar-excel/', views.exportar_excel_coordinador, name='exportar_excel_coordinador'),
] 