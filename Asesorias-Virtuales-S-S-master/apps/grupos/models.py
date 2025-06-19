from django.db import models
from django.conf import settings
from apps.componentes.models import Componente
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta

# class Grupo(models.Model):
#     componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='grupos')

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=20, unique=True)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='grupos')
    asesor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grupos_asesor')
    aprendices = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='grupos_aprendiz', limit_choices_to={'role': 'aprendiz'})
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f'{self.nombre} - {self.componente.nombre}'

    def clean(self):
        if self.aprendices.count() > 15:
            raise ValidationError('Se alcanzó el límite de personas en el grupo (máximo 15).')
        if self.asesor and self.asesor.grupo_set.count() > 4:
            raise ValidationError('Se alcanzó el límite de grupos asignados a este asesor (máximo 4).')
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')

class Reunion(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='reuniones')
    fecha = models.DateField()
    hora = models.TimeField()
    enlace = models.URLField(help_text="Ingrese el enlace de la reunión (Google Meet, Zoom, Teams, etc.)")
    realizada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reunión'
        verbose_name_plural = 'Reuniones'
        ordering = ['-fecha', '-hora']
    
    def __str__(self):
        return f'Reunión {self.grupo.nombre} - {self.fecha} {self.hora}'

    def clean(self):
        # Validar que la fecha y hora no sean pasadas
        if self.fecha < timezone.now().date():
            raise ValidationError('No se pueden crear reuniones en fechas pasadas.')
        
        if self.fecha == timezone.now().date() and self.hora < timezone.now().time():
            raise ValidationError('No se pueden crear reuniones en horas pasadas.')
        
        # Validar límite de 3 links por día por asesor
        reuniones_hoy = Reunion.objects.filter(
            grupo__asesor=self.grupo.asesor,
            fecha=self.fecha
        ).exclude(id=self.id).count()
        
        if reuniones_hoy >= 3:
            raise ValidationError('Se ha alcanzado el límite de 3 reuniones por día para este asesor.') 