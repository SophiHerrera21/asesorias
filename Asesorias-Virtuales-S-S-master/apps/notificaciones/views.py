from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Notificacion
from apps.grupos.models import Grupo

@login_required
def notificaciones_asesor(request):
    if request.method == 'POST':
        grupo_id = request.POST.get('grupo')
        titulo = request.POST.get('titulo')
        mensaje = request.POST.get('mensaje')
        
        try:
            grupo = Grupo.objects.get(id=grupo_id, asesor=request.user)
            
            # Crear notificación
            notificacion = Notificacion.objects.create(
                titulo=titulo,
                mensaje=mensaje,
                grupo=grupo,
                remitente=request.user
            )
            
            # Enviar correos a todos los aprendices del grupo
            for aprendiz in grupo.aprendices.all():
                send_mail(
                    subject=f'S&S Asesorías - {titulo}',
                    message=f'''
                    Hola {aprendiz.get_full_name()},
                    
                    {mensaje}
                    
                    Saludos,
                    {request.user.get_full_name()}
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[aprendiz.email],
                    fail_silently=False,
                )
            
            messages.success(request, 'Notificación enviada exitosamente.')
            return redirect('notificaciones_asesor')
            
        except Grupo.DoesNotExist:
            messages.error(request, 'Grupo no encontrado.')
        except Exception as e:
            messages.error(request, f'Error al enviar la notificación: {str(e)}')
    
    # Obtener grupos del asesor y notificaciones enviadas
    grupos = Grupo.objects.filter(asesor=request.user)
    notificaciones = Notificacion.objects.filter(remitente=request.user).order_by('-fecha')
    
    context = {
        'grupos': grupos,
        'notificaciones': notificaciones
    }
    return render(request, 'notificaciones/notificaciones_asesor.html', context) 