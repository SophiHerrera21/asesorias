from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Count, Q, F
from django.http import HttpResponse
import xlsxwriter
from io import BytesIO
from apps.grupos.models import Grupo
from apps.pruebas.models import Prueba, EntregaPrueba
from apps.componentes.models import Componente
from apps.asesorias.models import Asesoria
from datetime import datetime, timedelta
from apps.pqrs.models import PQRS
from apps.usuarios.models import Usuario

def es_coordinador(user):
    return hasattr(user, 'role') and user.role == 'coordinador'

@login_required
@user_passes_test(es_coordinador)
def reportes_coordinador(request):
    grupo_id = request.GET.get('grupo')
    componente_id = request.GET.get('componente')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    grupos = Grupo.objects.all()
    if grupo_id:
        grupos = grupos.filter(id=grupo_id)

    componentes = Componente.objects.all()
    if componente_id:
        componentes = componentes.filter(id=componente_id)

    labels_desempeno = []
    data_desempeno = []
    labels_asistencia = []
    data_asistencia = []
    labels_entregas = []
    data_entregas = []
    labels_pqrs = []
    data_pqrs = []
    labels_bloqueos = []
    data_bloqueos = []

    for grupo in grupos:
        promedio = EntregaPrueba.objects.filter(
            prueba__grupo=grupo
        ).aggregate(promedio=Avg('calificacion'))['promedio'] or 0
        labels_desempeno.append(grupo.nombre)
        data_desempeno.append(round(promedio, 2))

        total_asesorias = Asesoria.objects.filter(grupo=grupo)
        if fecha_inicio:
            total_asesorias = total_asesorias.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            total_asesorias = total_asesorias.filter(fecha__lte=fecha_fin)
        total_asesorias_count = total_asesorias.count()
        asesorias_realizadas = total_asesorias.filter(realizada=True).count()
        porcentaje_asistencia = (asesorias_realizadas / total_asesorias_count * 100) if total_asesorias_count > 0 else 0
        labels_asistencia.append(grupo.nombre)
        data_asistencia.append(round(porcentaje_asistencia, 2))

        total_entregas = EntregaPrueba.objects.filter(prueba__grupo=grupo)
        if fecha_inicio:
            total_entregas = total_entregas.filter(fecha_entrega__gte=fecha_inicio)
        if fecha_fin:
            total_entregas = total_entregas.filter(fecha_entrega__lte=fecha_fin)
        total_entregas_count = total_entregas.count()
        entregas_a_tiempo = total_entregas.filter(fecha_entrega__lte=F('prueba__fecha_limite')).count()
        porcentaje_entregas = (entregas_a_tiempo / total_entregas_count * 100) if total_entregas_count > 0 else 0
        labels_entregas.append(grupo.nombre)
        data_entregas.append(round(porcentaje_entregas, 2))

        cantidad_pqrs = PQRS.objects.filter(grupo=grupo)
        if fecha_inicio:
            cantidad_pqrs = cantidad_pqrs.filter(fecha_creacion__gte=fecha_inicio)
        if fecha_fin:
            cantidad_pqrs = cantidad_pqrs.filter(fecha_creacion__lte=fecha_fin)
        labels_pqrs.append(grupo.nombre)
        data_pqrs.append(cantidad_pqrs.count())

        bloqueados = grupo.aprendices.filter(is_active=False).count()
        labels_bloqueos.append(grupo.nombre)
        data_bloqueos.append(bloqueados)

    context = {
        'grupos': grupos,
        'componentes': componentes,
        'grupo_sel': int(grupo_id) if grupo_id else None,
        'componente_sel': int(componente_id) if componente_id else None,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'labels_desempeno': labels_desempeno,
        'data_desempeno': data_desempeno,
        'labels_asistencia': labels_asistencia,
        'data_asistencia': data_asistencia,
        'labels_entregas': labels_entregas,
        'data_entregas': data_entregas,
        'labels_pqrs': labels_pqrs,
        'data_pqrs': data_pqrs,
        'labels_bloqueos': labels_bloqueos,
        'data_bloqueos': data_bloqueos,
    }
    return render(request, 'reportes/reportes_coordinador.html', context)

@login_required
@user_passes_test(es_coordinador)
def exportar_excel_coordinador(request):
    grupo_id = request.GET.get('grupo')
    componente_id = request.GET.get('componente')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    grupos = Grupo.objects.all()
    if grupo_id:
        grupos = grupos.filter(id=grupo_id)
    componentes = Componente.objects.all()
    if componente_id:
        componentes = componentes.filter(id=componente_id)

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Resumen')
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#0a2342',
        'font_color': 'white',
        'border': 1
    })
    headers = ['Grupo', 'Componente', 'Aprendices', 'Pruebas', 'Promedio Calificaciones',
              'Asesorías Realizadas', 'Porcentaje Asistencia', 'Entregas a Tiempo', 'PQRS', 'Bloqueados']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    row = 1
    for grupo in grupos:
        num_aprendices = grupo.aprendices.count()
        num_pruebas = Prueba.objects.filter(grupo=grupo).count()
        promedio = EntregaPrueba.objects.filter(
            prueba__grupo=grupo
        ).aggregate(promedio=Avg('calificacion'))['promedio'] or 0
        total_asesorias = Asesoria.objects.filter(grupo=grupo)
        if fecha_inicio:
            total_asesorias = total_asesorias.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            total_asesorias = total_asesorias.filter(fecha__lte=fecha_fin)
        asesorias_realizadas = total_asesorias.filter(realizada=True).count()
        total_asesorias_count = total_asesorias.count()
        porcentaje_asistencia = (asesorias_realizadas / total_asesorias_count * 100) if total_asesorias_count > 0 else 0
        total_entregas = EntregaPrueba.objects.filter(prueba__grupo=grupo)
        if fecha_inicio:
            total_entregas = total_entregas.filter(fecha_entrega__gte=fecha_inicio)
        if fecha_fin:
            total_entregas = total_entregas.filter(fecha_entrega__lte=fecha_fin)
        entregas_a_tiempo = total_entregas.filter(fecha_entrega__lte=F('prueba__fecha_limite')).count()
        cantidad_pqrs = PQRS.objects.filter(grupo=grupo)
        if fecha_inicio:
            cantidad_pqrs = cantidad_pqrs.filter(fecha_creacion__gte=fecha_inicio)
        if fecha_fin:
            cantidad_pqrs = cantidad_pqrs.filter(fecha_creacion__lte=fecha_fin)
        bloqueados = grupo.aprendices.filter(is_active=False).count()
        worksheet.write(row, 0, grupo.nombre)
        worksheet.write(row, 1, grupo.componente.nombre)
        worksheet.write(row, 2, num_aprendices)
        worksheet.write(row, 3, num_pruebas)
        worksheet.write(row, 4, round(promedio, 2))
        worksheet.write(row, 5, asesorias_realizadas)
        worksheet.write(row, 6, f"{round(porcentaje_asistencia, 2)}%")
        worksheet.write(row, 7, entregas_a_tiempo)
        worksheet.write(row, 8, cantidad_pqrs.count())
        worksheet.write(row, 9, bloqueados)
        row += 1
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 30)
    worksheet.set_column('C:J', 15)
    workbook.close()
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=reporte_coordinador.xlsx'
    return response 