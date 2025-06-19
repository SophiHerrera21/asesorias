from django.db import models
from apps.grupos.models import Grupo
from apps.componentes.models import Componente

# class Asesoria(models.Model):
#     componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='asesorias')

class Asesoria(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='asesorias')
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='asesorias')
    fecha = models.DateField()
    hora = models.TimeField()
    realizada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    link_videollamada = models.URLField('Enlace de videollamada', max_length=500, default='https://meet.google.com/')
    
    class Meta:
        verbose_name = 'Asesoría'
        verbose_name_plural = 'Asesorías'
        ordering = ['-fecha', '-hora']
    
    def __str__(self):
        return f'Asesoría {self.grupo.nombre} - {self.fecha} {self.hora}' 