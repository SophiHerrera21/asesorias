from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class RegistroAuditoria(models.Model):
    TIPOS_ACCION = (
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
        ('create', 'Creación'),
        ('update', 'Actualización'),
        ('delete', 'Eliminación'),
        ('block', 'Bloqueo'),
        ('unblock', 'Desbloqueo'),
        ('grade', 'Calificación'),
        ('schedule', 'Programación'),
        ('upload', 'Subida de archivo'),
        ('download', 'Descarga de archivo'),
        ('email', 'Envío de correo'),
        ('report', 'Generación de reporte'),
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='acciones_auditoria')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tipo_accion = models.CharField(max_length=20, choices=TIPOS_ACCION)
    descripcion = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    # Para relacionar con cualquier modelo
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Datos adicionales en formato JSON
    datos_adicionales = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'Registro de auditoría'
        verbose_name_plural = 'Registros de auditoría'
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['usuario', 'fecha_hora']),
            models.Index(fields=['tipo_accion', 'fecha_hora']),
        ]

    def __str__(self):
        return f"{self.get_tipo_accion_display()} por {self.usuario} - {self.fecha_hora}"

    @classmethod
    def registrar(cls, usuario, tipo_accion, descripcion, ip_address=None, user_agent=None, 
                 content_object=None, datos_adicionales=None):
        """
        Método de clase para facilitar el registro de auditoría
        """
        registro = cls(
            usuario=usuario,
            tipo_accion=tipo_accion,
            descripcion=descripcion,
            ip_address=ip_address,
            user_agent=user_agent,
            datos_adicionales=datos_adicionales
        )
        
        if content_object:
            registro.content_type = ContentType.objects.get_for_model(content_object)
            registro.object_id = content_object.id
            
        registro.save()
        return registro 