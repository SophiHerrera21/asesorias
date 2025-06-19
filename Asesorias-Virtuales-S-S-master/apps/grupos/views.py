from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Grupo, Reunion
from datetime import timedelta
from django.utils import timezone

@login_required
def grupos_asesor(request):
    grupos = Grupo.objects.filter(asesor=request.user).prefetch_related('aprendices')
    return render(request, 'grupos/grupos_asesor.html', {'grupos': grupos})

@login_required
def programar_reunion(request):
    if request.method == 'POST':
        grupo_id = request.POST.get('grupo')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        enlace = request.POST.get('enlace')
        
        try:
            grupo = Grupo.objects.get(id=grupo_id, asesor=request.user)
            
            # Crear reunión
            reunion = Reunion.objects.create(
                grupo=grupo,
                fecha=fecha,
                hora=hora,
                enlace=enlace
            )
            
            # Enviar correos a todos los aprendices del grupo
            for aprendiz in grupo.aprendices.all():
                send_mail(
                    subject='S&S Asesorías - Nueva reunión programada',
                    message=f'''
                    Hola {aprendiz.get_full_name()},
                    
                    Se ha programado una nueva reunión para el grupo {grupo.nombre}.
                    
                    Fecha: {fecha}
                    Hora: {hora}
                    Enlace: {enlace}
                    
                    Saludos,
                    {request.user.get_full_name()}
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[aprendiz.email],
                    fail_silently=False,
                )
            
            messages.success(request, 'Reunión programada exitosamente.')
            return redirect('grupos_asesor')
            
        except Grupo.DoesNotExist:
            messages.error(request, 'Grupo no encontrado.')
        except Exception as e:
            messages.error(request, f'Error al programar la reunión: {str(e)}')
    
    return redirect('grupos_asesor')

@login_required
def eliminar_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id, asesor=request.user)
    
    try:
        # Enviar correo a los aprendices antes de eliminar el grupo
        for aprendiz in grupo.aprendices.all():
            send_mail(
                subject='S&S Asesorías - Grupo eliminado',
                message=f'''
                Hola {aprendiz.get_full_name()},
                
                El grupo {grupo.nombre} ha sido eliminado.
                Serás reasignado a un nuevo grupo próximamente.
                
                Saludos,
                {request.user.get_full_name()}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[aprendiz.email],
                fail_silently=False,
            )
        
        grupo.delete()
        messages.success(request, 'Grupo eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar el grupo: {str(e)}')
    
    return redirect('grupos_asesor')

@login_required
def finalizar_asesoria(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id, asesor=request.user)
    hoy = timezone.now().date()
    if grupo.estado == 'inactivo':
        messages.info(request, 'La asesoría ya está finalizada.')
        return redirect('grupos_asesor')
    if not grupo.fecha_inicio or hoy < grupo.fecha_inicio + timedelta(days=30):
        messages.error(request, f'No puedes finalizar la asesoría antes de {grupo.fecha_inicio + timedelta(days=30)}.')
        return redirect('grupos_asesor')
    if request.method == 'POST':
        grupo.estado = 'inactivo'
        grupo.save()
        # Notificar a todos los integrantes
        emails = [a.email for a in grupo.aprendices.all()]
        emails.append(grupo.asesor.email)
        # Si hay coordinador, agregar su correo (ajustar según tu modelo de coordinador)
        # emails.append(coordinador.email)
        send_mail(
            subject='Asesoría finalizada - S&S Asesorías Virtuales',
            message=f'La asesoría del grupo {grupo.nombre} ha finalizado. Ya no se podrán enviar mensajes ni asignar nuevas pruebas. Gracias por participar.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails,
            fail_silently=False,
        )
        messages.success(request, 'La asesoría se finalizó correctamente y se notificó a todos los integrantes.')
        return redirect('grupos_asesor')
    # GET: mostrar confirmación
    return render(request, 'grupos/confirmar_finalizar_asesoria.html', {'grupo': grupo, 'fecha_minima': grupo.fecha_inicio + timedelta(days=30)}) 