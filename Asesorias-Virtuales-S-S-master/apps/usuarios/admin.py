from django.contrib import admin
from .models import Usuario, CodigoRecuperacion, Configuracion, Asesor, Aprendiz, Coordinador, Grupo, Prueba, Notificacion, Reunion

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')

@admin.register(CodigoRecuperacion)
class CodigoRecuperacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'codigo', 'fecha_creacion', 'usado')
    list_filter = ('usado', 'fecha_creacion')
    search_fields = ('usuario__email', 'codigo')

@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ('nombre_institucion', 'email', 'telefono')
    fieldsets = (
        ('Información Institucional', {
            'fields': ('nombre_institucion', 'direccion', 'telefono', 'email', 'logo')
        }),
        ('Parámetros Generales', {
            'fields': ('tiempo_sesion', 'max_intentos_login', 'tiempo_bloqueo', 'max_tamano_archivo', 'tipos_archivo')
        }),
    )

@admin.register(Asesor)
class AsesorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidad', 'titulo', 'activo')
    list_filter = ('activo', 'trimestre')
    search_fields = ('usuario__email', 'usuario__first_name', 'usuario__last_name')

@admin.register(Aprendiz)
class AprendizAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ficha', 'programa', 'trimestre')
    list_filter = ('programa', 'trimestre')
    search_fields = ('usuario__email', 'usuario__first_name', 'usuario__last_name', 'ficha')

@admin.register(Coordinador)
class CoordinadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cargo', 'departamento')
    search_fields = ('usuario__email', 'usuario__first_name', 'usuario__last_name')

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'asesor', 'fecha_creacion', 'activo')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('nombre', 'asesor__usuario__email')

@admin.register(Prueba)
class PruebaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'grupo', 'fecha_creacion', 'fecha_limite')
    list_filter = ('fecha_creacion', 'fecha_limite')
    search_fields = ('titulo', 'grupo__nombre')

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'fecha_creacion', 'leida')
    list_filter = ('leida', 'fecha_creacion')
    search_fields = ('usuario__email', 'titulo')

@admin.register(Reunion)
class ReunionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'grupo', 'fecha', 'duracion')
    list_filter = ('fecha',)
    search_fields = ('titulo', 'grupo__nombre') 