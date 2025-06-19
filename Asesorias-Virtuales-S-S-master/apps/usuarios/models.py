from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import random
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    ROLES = (
        ('aprendiz', 'Aprendiz'),
        ('asesor', 'Asesor'),
        ('coordinador', 'Coordinador'),
    )
    role = models.CharField(max_length=20, choices=ROLES)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    imagen_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    documento = models.CharField(max_length=30, unique=True, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('bloqueado', 'Bloqueado'), ('inactivo', 'Inactivo')], default='activo')
    fecha_bloqueo = models.DateTimeField(null=True, blank=True)
    motivo_bloqueo = models.TextField(null=True, blank=True)
    correo_recuperacion = models.EmailField(null=True, blank=True)
    
    # Campos requeridos
    REQUIRED_FIELDS = ['email', 'role']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_role_display(self):
        return dict(self.ROLES).get(self.role, self.role)

    def perfil_completo(self):
        return all([
            self.first_name,
            self.last_name,
            self.email,
            self.telefono,
            self.direccion
        ])

    def bloquear_usuario(self, motivo, coordinador):
        self.estado = 'bloqueado'
        self.fecha_bloqueo = timezone.now()
        self.motivo_bloqueo = motivo
        self.save()

        # Enviar correo de notificación
        send_mail(
            subject='S&S Asesorías - Cuenta bloqueada',
            message=f'''
            Estimado/a {self.get_full_name()},

            Su cuenta ha sido bloqueada por el siguiente motivo:
            {motivo}

            Si desea recuperar su cuenta, por favor escriba a: {settings.ADMIN_EMAIL}

            Atentamente,
            Equipo S&S Asesorías
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            fail_silently=False,
        )

    def desbloquear_usuario(self, coordinador):
        self.estado = 'activo'
        self.fecha_bloqueo = None
        self.motivo_bloqueo = None
        self.save()

        # Enviar correo de notificación
        send_mail(
            subject='S&S Asesorías - Cuenta desbloqueada',
            message=f'''
            Estimado/a {self.get_full_name()},

            Su cuenta ha sido desbloqueada y ya puede acceder nuevamente al sistema.

            Atentamente,
            Equipo S&S Asesorías
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            fail_silently=False,
        )

class Configuracion(models.Model):
    nombre_institucion = models.CharField(max_length=100, default='S&S Asesorías Virtuales')
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to='config/', null=True, blank=True)
    
    # Parámetros generales
    tiempo_sesion = models.IntegerField(default=30, help_text='Tiempo máximo de sesión en minutos')
    max_intentos_login = models.IntegerField(default=3, help_text='Número máximo de intentos de inicio de sesión')
    tiempo_bloqueo = models.IntegerField(default=30, help_text='Tiempo de bloqueo por intentos fallidos en minutos')
    max_tamano_archivo = models.IntegerField(default=5, help_text='Tamaño máximo de archivos en MB')
    tipos_archivo = models.CharField(max_length=100, default='pdf,doc,docx', help_text='Tipos de archivo permitidos separados por comas')
    
    class Meta:
        verbose_name = 'Configuración'
        verbose_name_plural = 'Configuraciones'
    
    def __str__(self):
        return self.nombre_institucion

class CodigoRecuperacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    usado = models.BooleanField(default=False)
    
    @classmethod
    def generar_codigo(cls):
        return ''.join(random.choices('0123456789', k=6))
    
    def es_valido(self):
        return not self.usado and (timezone.now() - self.fecha_creacion).total_seconds() < 3600

class Asesor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    experiencia = models.TextField()
    titulo = models.CharField(max_length=100)
    max_grupos = models.IntegerField(default=4)
    disponibilidad = models.TextField()
    activo = models.BooleanField(default=True)
    trimestre = models.CharField(max_length=20, choices=[
        ('1', 'Primer Trimestre'),
        ('2', 'Segundo Trimestre'),
        ('3', 'Tercer Trimestre'),
        ('4', 'Cuarto Trimestre')
    ], default='1')
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.especialidad}"

class Aprendiz(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    ficha = models.CharField(max_length=20)
    programa = models.CharField(max_length=100)
    trimestre = models.CharField(max_length=20, choices=[
        ('1', 'Primer Trimestre'),
        ('2', 'Segundo Trimestre'),
        ('3', 'Tercer Trimestre'),
        ('4', 'Cuarto Trimestre')
    ], default='1')
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.programa}"

class Coordinador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.cargo}"

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    asesor = models.ForeignKey(Asesor, on_delete=models.CASCADE, related_name='grupos')
    aprendices = models.ManyToManyField(Aprendiz, related_name='grupos')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)
    max_aprendices = models.IntegerField(default=15)
    
    def __str__(self):
        return f"{self.nombre} - {self.asesor.usuario.get_full_name()}"

class Prueba(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_limite = models.DateTimeField()
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='pruebas')
    
    def __str__(self):
        return f"{self.titulo} - {self.grupo.nombre}"

class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    leida = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.get_full_name()}"

class Reunion(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    duracion = models.IntegerField(help_text='Duración en minutos')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='reuniones')
    link = models.URLField()
    
    def __str__(self):
        return f"{self.titulo} - {self.grupo.nombre}"