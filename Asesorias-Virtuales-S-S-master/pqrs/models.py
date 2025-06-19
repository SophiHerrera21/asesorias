from django.db import models
from django.utils.translation import gettext_lazy as _

class PQRS(models.Model):
    id_pqrs = models.AutoField(primary_key=True)
    pqrs = models.CharField(max_length=250)
    id_coordinador = models.ForeignKey('users.Coordinador', on_delete=models.SET_NULL, null=True, related_name='pqrs')
    id_asesoria = models.ForeignKey('asesorias.Asesoria', on_delete=models.SET_NULL, null=True, related_name='pqrs')
    id_usuario = models.ForeignKey('users.Usuario', on_delete=models.CASCADE, related_name='pqrs')
    tipo = models.CharField(max_length=20, choices=[('peticion', 'Petición'), ('queja', 'Queja'), ('reclamo', 'Reclamo'), ('sugerencia', 'Sugerencia'), ('reporte', 'Reporte')], default='reporte')
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=[('abierto', 'Abierto'), ('en_proceso', 'En Proceso'), ('resuelto', 'Resuelto'), ('cerrado', 'Cerrado')], default='abierto')
    prioridad = models.CharField(max_length=20, choices=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta'), ('critica', 'Crítica')], default='media')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    usuario_reportado = models.ForeignKey('users.Usuario', on_delete=models.SET_NULL, null=True, related_name='reportes')

    class Meta:
        db_table = 'pqrs'
        verbose_name = _('pqrs')
        verbose_name_plural = _('pqrs')

    def __str__(self):
        return f"PQRS: {self.asunto} - {self.tipo}"


class Respuesta(models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    respuesta = models.CharField(max_length=250)
    id_pregunta = models.ForeignKey(PQRS, on_delete=models.CASCADE, related_name='respuestas')
    id_coordinador = models.ForeignKey('users.Coordinador', on_delete=models.CASCADE, related_name='respuestas')
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('enviada', 'Enviada'), ('leida', 'Leída')], default='enviada')

    class Meta:
        db_table = 'respuesta'
        verbose_name = _('respuesta')
        verbose_name_plural = _('respuestas')

    def __str__(self):
        return f"Respuesta: {self.id_pregunta.asunto} - {self.fecha_respuesta}"
