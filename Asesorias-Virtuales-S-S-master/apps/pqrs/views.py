from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import PQRS, RespuestaPQRS
from .forms import PQRSForm, RespuestaPQRSForm
from django.http import HttpResponse
import xlsxwriter
from io import BytesIO
from django.contrib.auth.models import User
from apps.notificaciones.models import Notificacion

def es_coordinador(user):
    return user.role == 'coordinador'

def es_aprendiz(user):
    return user.role == 'aprendiz'

def es_asesor(user):
    return user.role == 'asesor'

@login_required
@user_passes_test(es_coordinador)
def pqrs_coordinador(request):
    # Obtener parámetros de búsqueda
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    
    # Filtrar PQRS
    pqrs_list = PQRS.objects.all()
    if query:
        pqrs_list = pqrs_list.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(usuario__email__icontains=query)
        )
    if tipo:
        pqrs_list = pqrs_list.filter(tipo=tipo)
    if estado:
        pqrs_list = pqrs_list.filter(estado=estado)
    if fecha_inicio:
        pqrs_list = pqrs_list.filter(fecha_creacion__gte=fecha_inicio)
    if fecha_fin:
        pqrs_list = pqrs_list.filter(fecha_creacion__lte=fecha_fin)
    pqrs_list = pqrs_list.order_by('-fecha_creacion')
    context = {
        'pqrs_list': pqrs_list,
        'query': query,
        'tipo': tipo,
        'estado': estado,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'tipos_pqrs': PQRS.TIPOS,
        'estados_pqrs': PQRS.ESTADOS,
    }
    return render(request, 'pqrs/pqrs_coordinador.html', context)

@login_required
@user_passes_test(es_coordinador)
def responder_pqrs(request, pqrs_id):
    pqrs = get_object_or_404(PQRS, id=pqrs_id)
    if request.method == 'POST':
        form = RespuestaPQRSForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.pqrs = pqrs
            respuesta.usuario = request.user
            respuesta.es_coordinador = True
            respuesta.save()
            pqrs.estado = 'resuelto'
            pqrs.save()
            # Notificación al aprendiz
            Notificacion.objects.create(
                usuario=pqrs.usuario,
                titulo=f'Respuesta a tu PQRS: {pqrs.titulo}',
                mensaje=f'Has recibido una respuesta a tu PQRS: {respuesta.mensaje}',
                url=''  # Puedes poner la URL a la PQRS si tienes una vista de detalle
            )
            # Enviar correo de notificación
            send_mail(
                subject=f'S&S Asesorías - Respuesta a tu {pqrs.get_tipo_display()}',
                message=f"""
                Hola {pqrs.usuario.get_full_name()},
                Hemos respondido a tu {pqrs.get_tipo_display().lower()}:
                Título: {pqrs.titulo}
                Respuesta: {respuesta.mensaje}
                Saludos,
                Equipo S&S
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[pqrs.usuario.email],
                fail_silently=False,
            )
            messages.success(request, 'Respuesta enviada exitosamente.')
            return redirect('pqrs:pqrs_coordinador')
    else:
        form = RespuestaPQRSForm()
    respuestas = RespuestaPQRS.objects.filter(pqrs=pqrs).order_by('fecha_creacion')
    return render(request, 'pqrs/responder_pqrs.html', {'pqrs': pqrs, 'form': form, 'respuestas': respuestas})

@login_required
@user_passes_test(es_coordinador)
def cambiar_estado_pqrs(request, pqrs_id):
    pqrs = get_object_or_404(PQRS, id=pqrs_id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(PQRS.ESTADOS):
            pqrs.estado = nuevo_estado
            pqrs.save()
            
            # Enviar correo de notificación
            send_mail(
                subject=f'S&S Asesorías - Estado de tu {pqrs.get_tipo_display()} actualizado',
                message=f'''
                Hola {pqrs.usuario.get_full_name()},
                
                El estado de tu {pqrs.get_tipo_display().lower()} ha sido actualizado a: {pqrs.get_estado_display()}
                
                Título: {pqrs.titulo}
                
                Saludos,
                Equipo S&S
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[pqrs.usuario.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Estado actualizado exitosamente.')
    
    return redirect('pqrs:pqrs_coordinador')

@login_required
@user_passes_test(es_asesor)
def pqrs_asesor(request):
    # Obtener PQRS de aprendices asignados al asesor
    pqrs_list = PQRS.objects.filter(usuario__role='aprendiz').order_by('-fecha_creacion')
    return render(request, 'pqrs/pqrs_asesor.html', {'pqrs_list': pqrs_list})

@login_required
@user_passes_test(es_aprendiz)
def pqrs_aprendiz(request):
    # Obtener PQRS del aprendiz
    pqrs_list = PQRS.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    if request.method == 'POST':
        form = PQRSForm(request.POST)
        if form.is_valid():
            pqrs = form.save(commit=False)
            pqrs.usuario = request.user
            pqrs.save()
            # Notificar a los coordinadores
            coordinadores = User.objects.filter(role='coordinador')
            if coordinadores.exists():
                for c in coordinadores:
                    Notificacion.objects.create(
                        usuario=c,
                        titulo=f'Nueva PQRS de {request.user.get_full_name()}',
                        mensaje=f'El aprendiz {request.user.get_full_name()} ha enviado una nueva PQRS: {pqrs.titulo}',
                        url=''  # Puedes poner la URL a la PQRS si tienes una vista de detalle
                    )
                send_mail(
                    subject=f'Nueva PQRS - {pqrs.titulo}',
                    message=f'''
                    El aprendiz {request.user.get_full_name()} ha enviado una nueva PQRS.
                    Tipo: {pqrs.get_tipo_display()}
                    Título: {pqrs.titulo}
                    Descripción: {pqrs.descripcion}
                    Por favor, revisa y responde la PQRS en el sistema.
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[c.email for c in coordinadores],
                    fail_silently=False,
                )
            messages.success(request, 'PQRS enviada exitosamente.')
            return redirect('pqrs:pqrs_aprendiz')
    else:
        form = PQRSForm()
    
    return render(request, 'pqrs/pqrs_aprendiz.html', {
        'pqrs_list': pqrs_list,
        'form': form
    })

@login_required
@user_passes_test(es_aprendiz)
def detalle_pqrs(request, pqrs_id):
    pqrs = get_object_or_404(PQRS, id=pqrs_id, usuario=request.user)
    return render(request, 'pqrs/detalle_pqrs.html', {'pqrs': pqrs})

@login_required
@user_passes_test(es_coordinador)
def exportar_excel(request):
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    pqrs_list = PQRS.objects.all()
    if query:
        pqrs_list = pqrs_list.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(usuario__email__icontains=query)
        )
    if tipo:
        pqrs_list = pqrs_list.filter(tipo=tipo)
    if estado:
        pqrs_list = pqrs_list.filter(estado=estado)
    if fecha_inicio:
        pqrs_list = pqrs_list.filter(fecha_creacion__gte=fecha_inicio)
    if fecha_fin:
        pqrs_list = pqrs_list.filter(fecha_creacion__lte=fecha_fin)
    pqrs_list = pqrs_list.order_by('-fecha_creacion')

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('PQRS')
    bold = workbook.add_format({'bold': True})

    headers = [
        'Usuario', 'Correo', 'Título', 'Tipo', 'Estado',
        'Fecha creación', 'Descripción'
    ]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, bold)

    for row, pqrs in enumerate(pqrs_list, start=1):
        worksheet.write(row, 0, pqrs.usuario.get_full_name())
        worksheet.write(row, 1, pqrs.usuario.email)
        worksheet.write(row, 2, pqrs.titulo)
        worksheet.write(row, 3, pqrs.get_tipo_display())
        worksheet.write(row, 4, pqrs.get_estado_display())
        worksheet.write(row, 5, pqrs.fecha_creacion.strftime('%d/%m/%Y %H:%M'))
        worksheet.write(row, 6, pqrs.descripcion)

    workbook.close()
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=PQRS.xlsx'
    return response 