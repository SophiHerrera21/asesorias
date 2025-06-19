from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from asesorias_virtuales.utils.email_utils import send_welcome_email
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Prueba el sistema de correos de bienvenida'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email específico para enviar la prueba (opcional)',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Mostrar información detallada',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Iniciando prueba del sistema de correos de bienvenida...')
        )
        
        # Verificar configuración
        self.stdout.write('\n🔧 Verificando configuración de email:')
        self.check_email_configuration()
        
        # Buscar usuario para la prueba
        user = self.get_test_user(options['email'])
        if not user:
            return
        
        # Enviar correo de prueba
        self.stdout.write(f'\n📧 Enviando correo de bienvenida a: {user.email}')
        self.stdout.write(f'👤 Usuario: {user.get_full_name()}')
        self.stdout.write(f'🎭 Rol: {user.get_role_display()}')
        
        if options['verbose']:
            self.stdout.write(f'📅 Fecha de registro: {user.fecha_registro}')
            self.stdout.write(f'📱 Teléfono: {user.telefono or "No registrado"}')
            self.stdout.write(f'📍 Dirección: {user.direccion or "No registrada"}')
        
        # Enviar correo
        result = send_welcome_email(user)
        
        if result:
            self.stdout.write(
                self.style.SUCCESS('\n✅ Correo de bienvenida enviado exitosamente')
            )
            self.stdout.write(
                self.style.WARNING('\n💡 Verifica la bandeja de entrada (y spam) del correo')
            )
        else:
            self.stdout.write(
                self.style.ERROR('\n❌ Error al enviar el correo de bienvenida')
            )
            self.stdout.write(
                self.style.WARNING('\n🔍 Revisa los logs de Django para más detalles')
            )

    def check_email_configuration(self):
        """Verifica la configuración de email"""
        required_settings = [
            'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_HOST_USER', 
            'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL'
        ]
        
        all_configured = True
        for setting in required_settings:
            value = getattr(settings, setting, None)
            if value:
                self.stdout.write(f'   ✅ {setting}: {value}')
            else:
                self.stdout.write(f'   ❌ {setting}: No configurado')
                all_configured = False
        
        if all_configured:
            self.stdout.write(
                self.style.SUCCESS('   ✅ Configuración de email completa')
            )
        else:
            self.stdout.write(
                self.style.ERROR('   ❌ Configuración de email incompleta')
            )
            return False
        
        return True

    def get_test_user(self, email=None):
        """Obtiene un usuario para la prueba"""
        if email:
            try:
                user = User.objects.get(email=email)
                return user
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ No se encontró un usuario con el email: {email}')
                )
                return None
        
        # Buscar el primer usuario disponible
        user = User.objects.first()
        if not user:
            self.stdout.write(
                self.style.ERROR('❌ No se encontraron usuarios en la base de datos')
            )
            self.stdout.write(
                self.style.WARNING('💡 Crea un usuario primero usando el registro o el admin')
            )
            return None
        
        return user 