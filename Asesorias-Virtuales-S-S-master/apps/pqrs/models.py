from django.db import models
from django.conf import settings
from apps.grupos.models import Grupo
from apps.usuarios.models import Usuario
from django.contrib.auth.models import User

class PQRS(models.Model):
    TIPOS = [
        ('peticion', 'Petición'),
        ('queja', 'Queja'),
        ('reclamo', 'Reclamo'),
        ('sugerencia', 'Sugerencia'),
    ]
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True,  # Permitir nulo temporalmente
        blank=True  # Permitir en blanco en formularios
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'PQRS'
        verbose_name_plural = 'PQRS'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f'PQRS #{self.id} - {self.get_tipo_display()}'

class RespuestaPQRS(models.Model):
    pqrs = models.ForeignKey(PQRS, on_delete=models.CASCADE, related_name='respuestas')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True,  # Permitir nulo temporalmente
        blank=True  # Permitir en blanco en formularios
    )
    mensaje = models.TextField()
    es_coordinador = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Respuesta PQRS'
        verbose_name_plural = 'Respuestas PQRS'
        ordering = ['fecha_creacion']
    
    def __str__(self):
        return f'Respuesta a PQRS #{self.pqrs.id}' 