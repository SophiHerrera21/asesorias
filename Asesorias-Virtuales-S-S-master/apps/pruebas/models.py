from django.db import models
from django.conf import settings
from apps.grupos.models import Grupo
from apps.componentes.models import Componente
from django.core.exceptions import ValidationError
from django.utils import timezone
import os

class Prueba(models.Model):
    nombre = models.CharField(max_length=200)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='pruebas')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='pruebas')
    fecha_limite = models.DateTimeField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_reagendada = models.DateTimeField(null=True, blank=True)
    motivo_reagendamiento = models.TextField(null=True, blank=True)
    notificacion_enviada = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Prueba'
        verbose_name_plural = 'Pruebas'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f'{self.nombre} - {self.grupo.nombre}'

    def clean(self):
        # Validar que la fecha límite no sea pasada
        if self.fecha_limite < timezone.now():
            raise ValidationError('No se pueden crear pruebas con fecha límite pasada.')
        
        # Si es una reagendación, validar que la nueva fecha sea futura
        if self.fecha_reagendada and self.fecha_reagendada < timezone.now():
            raise ValidationError('No se pueden reagendar pruebas para fechas pasadas.')

def entrega_prueba_upload_to(instance, filename):
    fecha = timezone.now()
    ext = filename.split('.')[-1]
    nombre = f"{instance.prueba.nombre}_{instance.aprendiz.id}_{fecha.strftime('%Y%m%d_%H%M%S')}.{ext}"
    return f"entregas/{fecha.year}/{fecha.month}/{nombre}"

class EntregaPrueba(models.Model):
    prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE, related_name='entregas')
    aprendiz = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entregas_prueba')
    archivo = models.FileField(upload_to=entrega_prueba_upload_to)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fecha_entrega = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Entrega de prueba'
        verbose_name_plural = 'Entregas de pruebas'
        ordering = ['-fecha_entrega']
    
    def __str__(self):
        return f'Entrega de {self.aprendiz.get_full_name()} - {self.prueba.nombre}'

    def clean(self):
        # Validar que la entrega no sea después de la fecha límite
        if self.prueba.fecha_reagendada:
            fecha_limite = self.prueba.fecha_reagendada
        else:
            fecha_limite = self.prueba.fecha_limite
        if timezone.now() > fecha_limite:
            raise ValidationError('No se pueden realizar entregas después de la fecha límite.')
        # Validar solo PDF
        if self.archivo:
            ext = os.path.splitext(self.archivo.name)[1].lower()
            if ext != '.pdf':
                raise ValidationError('Solo se permiten archivos PDF para la entrega.') 