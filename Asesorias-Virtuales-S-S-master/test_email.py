#!/usr/bin/env python
"""
Script de prueba para verificar el sistema de correos de bienvenida
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asesorias_virtuales.settings')
django.setup()

from django.contrib.auth import get_user_model
from asesorias_virtuales.utils.email_utils import send_welcome_email

User = get_user_model()

def test_welcome_email():
    """Prueba el envío de correo de bienvenida"""
    try:
        # Buscar un usuario existente para la prueba
        user = User.objects.first()
        if not user:
            print("❌ No se encontraron usuarios en la base de datos")
            return False
        
        print(f"📧 Enviando correo de bienvenida a: {user.email}")
        print(f"👤 Usuario: {user.get_full_name()}")
        print(f"🎭 Rol: {user.get_role_display()}")
        
        # Enviar correo de bienvenida
        result = send_welcome_email(user)
        
        if result:
            print("✅ Correo de bienvenida enviado exitosamente")
            return True
        else:
            print("❌ Error al enviar el correo de bienvenida")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        return False

def test_email_configuration():
    """Prueba la configuración de email"""
    from django.conf import settings
    
    print("🔧 Verificando configuración de email:")
    print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   SITE_URL: {getattr(settings, 'SITE_URL', 'No configurado')}")
    
    # Verificar que las configuraciones necesarias estén presentes
    required_settings = [
        'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_HOST_USER', 
        'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL'
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not hasattr(settings, setting) or not getattr(settings, setting):
            missing_settings.append(setting)
    
    if missing_settings:
        print(f"❌ Configuraciones faltantes: {', '.join(missing_settings)}")
        return False
    else:
        print("✅ Configuración de email completa")
        return True

if __name__ == '__main__':
    print("🚀 Iniciando pruebas del sistema de correos...")
    print("=" * 50)
    
    # Probar configuración
    config_ok = test_email_configuration()
    
    if config_ok:
        print("\n" + "=" * 50)
        # Probar envío de correo
        email_ok = test_welcome_email()
        
        if email_ok:
            print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        else:
            print("\n❌ Error en el envío de correos")
            sys.exit(1)
    else:
        print("\n❌ Error en la configuración de email")
        sys.exit(1) 