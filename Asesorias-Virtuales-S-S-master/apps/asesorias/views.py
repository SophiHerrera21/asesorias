from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Asesoria
from apps.usuarios.models import Usuario
from apps.grupos.models import Grupo
from apps.componentes.models import Componente
import xlsxwriter
from io import BytesIO
from django.http import HttpResponse
from .forms import AsesoriaForm

@login_required
def asesorias_asesor(request):
    # Obtener asesorías de los grupos del asesor
    asesorias = Asesoria.objects.filter(
        grupo__asesor=request.user
    ).select_related('grupo', 'componente').order_by('-fecha', '-hora')
    
    return render(request, 'asesorias/asesorias_asesor.html', {'asesorias': asesorias})

@login_required
def detalle_asesoria(request, asesoria_id):
    asesoria = get_object_or_404(Asesoria, id=asesoria_id, grupo__asesor=request.user)
    return render(request, 'asesorias/detalle_asesoria.html', {'asesoria': asesoria})

@login_required
def marcar_realizada(request, asesoria_id):
    asesoria = get_object_or_404(Asesoria, id=asesoria_id, grupo__asesor=request.user)
    
    try:
        asesoria.realizada = True
        asesoria.save()
        
        # Enviar correo a los aprendices
        for aprendiz in asesoria.grupo.aprendices.all():
            send_mail(
                subject='S&S Asesorías - Asesoría realizada',
                message=f'''
                Hola {aprendiz.get_full_name()},
                
                La asesoría programada para el grupo {asesoria.grupo.nombre} ha sido marcada como realizada.
                
                Fecha: {asesoria.fecha}
                Hora: {asesoria.hora}
                Componente: {asesoria.componente.nombre}
                Enlace de videollamada: {asesoria.link_videollamada}
                
                Saludos,
                {request.user.get_full_name()}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[aprendiz.email],
                fail_silently=False,
            )
        
        messages.success(request, 'Asesoría marcada como realizada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al marcar la asesoría como realizada: {str(e)}')
    
    return redirect('asesorias_asesor')

@login_required
def reagendar_asesoria(request, asesoria_id):
    asesoria = get_object_or_404(Asesoria, id=asesoria_id, grupo__asesor=request.user)
    
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        link = request.POST.get('link_videollamada')
        
        try:
            # Actualizar asesoría
            asesoria.fecha = fecha
            asesoria.hora = hora
            if link:
                asesoria.link_videollamada = link
            asesoria.save()
            
            # Enviar correo a los aprendices
            for aprendiz in asesoria.grupo.aprendices.all():
                send_mail(
                    subject='S&S Asesorías - Asesoría reagendada',
                    message=f'''
                    Hola {aprendiz.get_full_name()},
                    
                    La asesoría del grupo {asesoria.grupo.nombre} ha sido reagendada.
                    
                    Nueva fecha: {fecha}
                    Nueva hora: {hora}
                    Componente: {asesoria.componente.nombre}
                    Enlace de videollamada: {asesoria.link_videollamada}
                    
                    Saludos,
                    {request.user.get_full_name()}
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[aprendiz.email],
                    fail_silently=False,
                )
            
            messages.success(request, 'Asesoría reagendada exitosamente.')
            return redirect('asesorias_asesor')
            
        except Exception as e:
            messages.error(request, f'Error al reagendar la asesoría: {str(e)}')
    
    return redirect('asesorias_asesor')

@login_required
def cancelar_asesoria(request, asesoria_id):
    asesoria = get_object_or_404(Asesoria, id=asesoria_id, grupo__asesor=request.user)
    
    try:
        # Enviar correo a los aprendices antes de eliminar
        for aprendiz in asesoria.grupo.aprendices.all():
            send_mail(
                subject='S&S Asesorías - Asesoría cancelada',
                message=f'''
                Hola {aprendiz.get_full_name()},
                
                La asesoría programada para el grupo {asesoria.grupo.nombre} ha sido cancelada.
                
                Fecha original: {asesoria.fecha}
                Hora original: {asesoria.hora}
                Componente: {asesoria.componente.nombre}
                Enlace de videollamada: {asesoria.link_videollamada}
                
                Saludos,
                {request.user.get_full_name()}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[aprendiz.email],
                fail_silently=False,
            )
        
        asesoria.delete()
        messages.success(request, 'Asesoría cancelada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al cancelar la asesoría: {str(e)}')
    
    return redirect('asesorias_asesor')

def es_coordinador(user):
    return user.role == 'coordinador'

@login_required
@user_passes_test(es_coordinador)
def historial_asesorias_coordinador(request):
    grupos = Grupo.objects.all()
    componentes = Componente.objects.all()
    asesores = Usuario.objects.filter(role='asesor')
    estado = request.GET.get('estado', '')
    grupo_id = request.GET.get('grupo', '')
    componente_id = request.GET.get('componente', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    asesorias = Asesoria.objects.all().select_related('grupo', 'componente', 'grupo__asesor')
    if grupo_id:
        asesorias = asesorias.filter(grupo_id=grupo_id)
    if componente_id:
        asesorias = asesorias.filter(componente_id=componente_id)
    if estado:
        if estado == 'realizada':
            asesorias = asesorias.filter(realizada=True)
        elif estado == 'pendiente':
            asesorias = asesorias.filter(realizada=False)
    if fecha_inicio:
        asesorias = asesorias.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        asesorias = asesorias.filter(fecha__lte=fecha_fin)

    context = {
        'asesorias': asesorias,
        'grupos': grupos,
        'componentes': componentes,
        'asesores': asesores,
        'estado_sel': estado,
        'grupo_sel': grupo_id,
        'componente_sel': componente_id,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    return render(request, 'asesorias/historial_coordinador.html', context)

@login_required
@user_passes_test(es_coordinador)
def exportar_historial_asesorias(request):
    grupo_id = request.GET.get('grupo', '')
    componente_id = request.GET.get('componente', '')
    estado = request.GET.get('estado', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    asesorias = Asesoria.objects.all().select_related('grupo', 'componente', 'grupo__asesor')
    if grupo_id:
        asesorias = asesorias.filter(grupo_id=grupo_id)
    if componente_id:
        asesorias = asesorias.filter(componente_id=componente_id)
    if estado:
        if estado == 'realizada':
            asesorias = asesorias.filter(realizada=True)
        elif estado == 'pendiente':
            asesorias = asesorias.filter(realizada=False)
    if fecha_inicio:
        asesorias = asesorias.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        asesorias = asesorias.filter(fecha__lte=fecha_fin)
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Historial Asesorías')
    header_format = workbook.add_format({'bold': True, 'bg_color': '#0a2342', 'font_color': 'white', 'border': 1})
    headers = ['ID', 'Grupo', 'Componente', 'Asesor', 'Aprendices', 'Fecha', 'Hora', 'Estado', 'Enlace videollamada']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    row = 1
    for asesoria in asesorias:
        aprendices = ', '.join([a.get_full_name() for a in asesoria.grupo.aprendices.all()])
        worksheet.write(row, 0, asesoria.id)
        worksheet.write(row, 1, asesoria.grupo.nombre)
        worksheet.write(row, 2, asesoria.componente.nombre)
        worksheet.write(row, 3, asesoria.grupo.asesor.get_full_name() if asesoria.grupo.asesor else '')
        worksheet.write(row, 4, aprendices)
        worksheet.write(row, 5, str(asesoria.fecha))
        worksheet.write(row, 6, str(asesoria.hora))
        worksheet.write(row, 7, 'Realizada' if asesoria.realizada else 'Pendiente')
        worksheet.write(row, 8, asesoria.link_videollamada)
        row += 1
    worksheet.set_column('A:I', 20)
    workbook.close()
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=historial_asesorias.xlsx'
    return response

def enviar_correo_asesoria(asesoria, evento):
    # evento: 'creada', 'reagendada', 'cancelada'
    asunto = {
        'creada': 'S&S Asesorías Virtuales - Nueva asesoría programada',
        'reagendada': 'S&S Asesorías Virtuales - Asesoría reagendada',
        'cancelada': 'S&S Asesorías Virtuales - Asesoría cancelada',
    }[evento]
    estado = 'Cancelada' if evento == 'cancelada' else ('Pendiente' if not asesoria.realizada else 'Realizada')
    aprendices = ', '.join([a.get_full_name() for a in asesoria.grupo.aprendices.all()])
    mensaje = f"""
Hola,

Te informamos sobre una asesoría en el sistema S&S Asesorías Virtuales.

Datos de la asesoría:
- ID de la asesoría: {asesoria.id}
- Grupo: {asesoria.grupo.nombre}
- Componente: {asesoria.componente.nombre}
- Asesor: {asesoria.grupo.asesor.get_full_name() if asesoria.grupo.asesor else ''}
- Aprendices: {aprendices}
- Fecha: {asesoria.fecha}
- Hora: {asesoria.hora}
- Estado: {estado}
- Enlace de videollamada: {asesoria.link_videollamada}

Por favor, revisa estos datos y accede al enlace de videollamada en la fecha y hora indicadas.

Si tienes dudas o inconvenientes, comunícate con tu asesor o coordinador.

Saludos cordiales,
Equipo S&S Asesorías Virtuales

Este es un mensaje automático, no responder.
"""
    destinatarios = [a.email for a in asesoria.grupo.aprendices.all()]
    if asesoria.grupo.asesor:
        destinatarios.append(asesoria.grupo.asesor.email)
    # Coordinadores
    coordinadores = Usuario.objects.filter(role='coordinador').values_list('email', flat=True)
    destinatarios += list(coordinadores)
    send_mail(
        subject=asunto,
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=destinatarios,
        fail_silently=False,
    )

@login_required
def crear_asesoria(request):
    if request.method == 'POST':
        form = AsesoriaForm(request.POST)
        if form.is_valid():
            asesoria = form.save()
            enviar_correo_asesoria(asesoria, 'creada')
            messages.success(request, 'Asesoría creada y notificaciones enviadas.')
            return redirect('asesorias:asesorias_asesor')
    else:
        form = AsesoriaForm()
    return render(request, 'asesorias/crear_asesoria.html', {'form': form})

@login_required
def editar_asesoria(request, asesoria_id):
    asesoria = get_object_or_404(Asesoria, id=asesoria_id, grupo__asesor=request.user)
    if request.method == 'POST':
        form = AsesoriaForm(request.POST, instance=asesoria)
        if form.is_valid():
            asesoria = form.save()
            enviar_correo_asesoria(asesoria, 'reagendada')
            messages.success(request, 'Asesoría actualizada y notificaciones enviadas.')
            return redirect('asesorias:asesorias_asesor')
    else:
        form = AsesoriaForm(instance=asesoria)
    return render(request, 'asesorias/editar_asesoria.html', {'form': form, 'asesoria': asesoria})

@login_required
def cancelar_asesoria(request, asesoria_id):
    asesoria = get_object_or_404(Asesoria, id=asesoria_id, grupo__asesor=request.user)
    try:
        enviar_correo_asesoria(asesoria, 'cancelada')
        asesoria.delete()
        messages.success(request, 'Asesoría cancelada y notificaciones enviadas.')
    except Exception as e:
        messages.error(request, f'Error al cancelar la asesoría: {str(e)}')
    return redirect('asesorias:asesorias_asesor') 