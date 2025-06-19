from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Prueba, EntregaPrueba
from .forms import EntregaPruebaForm
import os

def es_aprendiz(user):
    return user.role == 'aprendiz'

@login_required
def pruebas_asesor(request):
    # Obtener pruebas de los grupos del asesor
    pruebas = Prueba.objects.filter(
        grupo__asesor=request.user
    ).select_related('grupo', 'componente').order_by('-fecha_creacion')
    
    # Obtener grupos y componentes para el formulario
    grupos = request.user.grupos_asesor.all()
    componentes = request.user.componentes_asesor.all()
    
    context = {
        'pruebas': pruebas,
        'grupos': grupos,
        'componentes': componentes
    }
    return render(request, 'pruebas/pruebas_asesor.html', context)

@login_required
def crear_prueba(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        componente_id = request.POST.get('componente')
        grupo_id = request.POST.get('grupo')
        fecha_limite = request.POST.get('fecha_limite')
        
        try:
            grupo = request.user.grupos_asesor.get(id=grupo_id)
            if grupo.estado == 'inactivo':
                messages.error(request, 'No se pueden asignar pruebas a un grupo cuya asesoría ha finalizado.')
                return redirect('pruebas_asesor')
            componente = request.user.componentes_asesor.get(id=componente_id)
            
            # Crear prueba
            prueba = Prueba.objects.create(
                nombre=nombre,
                componente=componente,
                grupo=grupo,
                fecha_limite=fecha_limite
            )
            
            # Enviar correo a los aprendices
            for aprendiz in grupo.aprendices.all():
                send_mail(
                    subject='S&S Asesorías - Nueva prueba asignada',
                    message=f'''
                    Hola {aprendiz.get_full_name()},
                    
                    Se ha creado una nueva prueba para tu grupo {grupo.nombre}.
                    
                    Nombre: {nombre}
                    Componente: {componente.nombre}
                    Fecha límite: {fecha_limite}
                    
                    Saludos,
                    {request.user.get_full_name()}
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[aprendiz.email],
                    fail_silently=False,
                )
            
            messages.success(request, 'Prueba creada exitosamente.')
            return redirect('pruebas_asesor')
            
        except Exception as e:
            messages.error(request, f'Error al crear la prueba: {str(e)}')
    
    return redirect('pruebas_asesor')

@login_required
def entregas_prueba(request, prueba_id):
    prueba = get_object_or_404(Prueba, id=prueba_id, grupo__asesor=request.user)
    entregas = EntregaPrueba.objects.filter(prueba=prueba).select_related('aprendiz')
    
    return render(request, 'pruebas/entregas_prueba.html', {
        'prueba': prueba,
        'entregas': entregas
    })

@login_required
def eliminar_prueba(request, prueba_id):
    prueba = get_object_or_404(Prueba, id=prueba_id, grupo__asesor=request.user)
    
    try:
        # Enviar correo a los aprendices antes de eliminar
        for aprendiz in prueba.grupo.aprendices.all():
            send_mail(
                subject='S&S Asesorías - Prueba eliminada',
                message=f'''
                Hola {aprendiz.get_full_name()},
                
                La prueba "{prueba.nombre}" ha sido eliminada.
                
                Grupo: {prueba.grupo.nombre}
                Componente: {prueba.componente.nombre}
                
                Saludos,
                {request.user.get_full_name()}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[aprendiz.email],
                fail_silently=False,
            )
        
        prueba.delete()
        messages.success(request, 'Prueba eliminada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar la prueba: {str(e)}')
    
    return redirect('pruebas_asesor')

@login_required
@user_passes_test(es_aprendiz)
def entregar_prueba(request, prueba_id):
    prueba = get_object_or_404(Prueba, id=prueba_id, grupo__aprendices=request.user)
    
    # Verificar si ya existe una entrega
    entrega_existente = EntregaPrueba.objects.filter(
        prueba=prueba,
        aprendiz=request.user
    ).first()
    
    # Verificar fecha límite
    fecha_limite = prueba.fecha_reagendada if prueba.fecha_reagendada else prueba.fecha_limite
    if timezone.now() > fecha_limite:
        messages.error(request, 'La fecha límite para entregar esta prueba ha expirado.')
        return redirect('pruebas_aprendiz')
    
    # Verificar intentos
    if entrega_existente and entrega_existente.intentos >= 3:
        messages.error(request, 'Has alcanzado el límite de 3 intentos para esta prueba.')
        return redirect('pruebas_aprendiz')
    
    if request.method == 'POST':
        form = EntregaPruebaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            
            # Validar tipo de archivo
            extension = os.path.splitext(archivo.name)[1].lower()
            if extension not in ['.pdf', '.doc', '.docx']:
                messages.error(request, 'Solo se permiten archivos PDF, DOC o DOCX.')
                return render(request, 'pruebas/entregar_prueba.html', {'form': form, 'prueba': prueba})
            
            # Validar tamaño (máximo 10MB)
            if archivo.size > 10 * 1024 * 1024:
                messages.error(request, 'El archivo no debe superar los 10MB.')
                return render(request, 'pruebas/entregar_prueba.html', {'form': form, 'prueba': prueba})
            
            # Crear o actualizar entrega
            if entrega_existente:
                entrega = entrega_existente
                entrega.archivo = archivo
                entrega.intentos += 1
                entrega.fecha_entrega = timezone.now()
            else:
                entrega = form.save(commit=False)
                entrega.prueba = prueba
                entrega.aprendiz = request.user
                entrega.intentos = 1
            
            entrega.save()
            
            # Notificar al asesor
            send_mail(
                subject=f'Nueva entrega de prueba - {prueba.nombre}',
                message=f'''
                El aprendiz {request.user.get_full_name()} ha entregado la prueba {prueba.nombre}.
                
                Grupo: {prueba.grupo.nombre}
                Fecha de entrega: {entrega.fecha_entrega}
                Intentos: {entrega.intentos}
                
                Por favor, revisa la entrega en el sistema.
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[prueba.grupo.asesor.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Prueba entregada exitosamente.')
            return redirect('pruebas_aprendiz')
    else:
        form = EntregaPruebaForm()
    
    return render(request, 'pruebas/entregar_prueba.html', {
        'form': form,
        'prueba': prueba,
        'intentos_restantes': 3 - (entrega_existente.intentos if entrega_existente else 0)
    }) 