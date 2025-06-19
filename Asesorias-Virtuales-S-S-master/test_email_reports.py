#!/usr/bin/env python
"""
Script de prueba para verificar el sistema de reportes de error de correos.
Prueba: envío de reportes, validación de formularios, envíos masivos.
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asesorias_virtuales.settings')
django.setup()

from asesorias_virtuales.utils.email_utils import send_error_report, send_mass_email, send_bulk_notifications
from apps.usuarios.forms import UsuarioForm

def test_error_report():
    """Prueba el envío de reportes de error"""
    print("📧 Probando envío de reportes de error...")
    
    try:
        # Probar envío de reporte de error
        result = send_error_report(
            subject='Prueba de reporte de error',
            message='Este es un reporte de prueba para verificar el sistema de notificaciones.',
            extra_data={
                'fecha': datetime.now().isoformat(),
                'tipo': 'prueba',
                'usuario': 'test@example.com'
            }
        )
        
        if result:
            print("✅ Reporte de error enviado correctamente")
        else:
            print("❌ Error al enviar reporte de error")
            
    except Exception as e:
        print(f"❌ Error en prueba de reporte: {e}")

def test_form_validation_error():
    """Prueba la validación de formularios con reporte de error"""
    print("\n📝 Probando validación de formulario con reporte...")
    
    # Crear datos de formulario con errores
    form_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'documento': '12345678',
        'role': 'aprendiz',
        'telefono': '123456789',
        'direccion': 'Test Address',
        'password1': '123',  # Contraseña muy corta
        'password2': '123'
    }
    
    form = UsuarioForm(data=form_data)
    if not form.is_valid():
        print("✅ Formulario detecta errores correctamente")
        
        # Simular envío de reporte de error
        error_msg = '\n'.join([f'{field}: {errors}' for field, errors in form.errors.items()])
        result = send_error_report(
            subject='Error de validación en registro de aprendiz',
            message=error_msg,
            extra_data=form_data
        )
        
        if result:
            print("✅ Reporte de error de validación enviado correctamente")
        else:
            print("❌ Error al enviar reporte de validación")
    else:
        print("❌ Error: El formulario debería detectar errores")

def test_mass_email_error():
    """Prueba envío masivo con reporte de error"""
    print("\n📨 Probando envío masivo con reporte de error...")
    
    # Probar envío masivo sin destinatarios
    result = send_mass_email(
        subject='Prueba de envío masivo',
        html_template='emails/welcome.html',
        context={'user': None},
        recipient_emails=[],  # Lista vacía para causar error
        email_type='prueba'
    )
    
    if not result['success']:
        print("✅ Envío masivo sin destinatarios reportado correctamente")
        print(f"   Errores: {result['errors']}")
    else:
        print("❌ Error: El envío masivo sin destinatarios debería fallar")

def test_bulk_notifications_error():
    """Prueba notificaciones masivas con reporte de error"""
    print("\n🔔 Probando notificaciones masivas con reporte...")
    
    # Probar notificaciones masivas sin notificaciones
    result = send_bulk_notifications(
        notifications=[],  # Lista vacía para causar error
        notification_type='prueba'
    )
    
    if not result['success']:
        print("✅ Notificaciones masivas sin datos reportado correctamente")
        print(f"   Errores: {result['errors']}")
    else:
        print("❌ Error: Las notificaciones masivas sin datos deberían fallar")

def test_email_configuration():
    """Verifica la configuración de correo"""
    print("\n⚙️ Verificando configuración de correo...")
    
    from django.conf import settings
    
    config_ok = True
    
    # Verificar configuración SMTP
    if not hasattr(settings, 'EMAIL_HOST') or not settings.EMAIL_HOST:
        print("❌ EMAIL_HOST no configurado")
        config_ok = False
    else:
        print(f"✅ EMAIL_HOST: {settings.EMAIL_HOST}")
    
    if not hasattr(settings, 'EMAIL_HOST_USER') or not settings.EMAIL_HOST_USER:
        print("❌ EMAIL_HOST_USER no configurado")
        config_ok = False
    else:
        print(f"✅ EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    
    if not hasattr(settings, 'DEFAULT_FROM_EMAIL') or not settings.DEFAULT_FROM_EMAIL:
        print("❌ DEFAULT_FROM_EMAIL no configurado")
        config_ok = False
    else:
        print(f"✅ DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    if not hasattr(settings, 'ADMIN_EMAIL') or not settings.ADMIN_EMAIL:
        print("❌ ADMIN_EMAIL no configurado")
        config_ok = False
    else:
        print(f"✅ ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
    
    return config_ok

def main():
    """Función principal que ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas del sistema de reportes de correo")
    print("=" * 60)
    
    try:
        # Verificar configuración
        config_ok = test_email_configuration()
        
        if config_ok:
            # Ejecutar pruebas
            test_error_report()
            test_form_validation_error()
            test_mass_email_error()
            test_bulk_notifications_error()
            
            print("\n" + "=" * 60)
            print("✅ Todas las pruebas completadas")
            print("📊 Resumen:")
            print("   - Reportes de error: Implementados")
            print("   - Validación de formularios: Con reporte")
            print("   - Envíos masivos: Con reporte de errores")
            print("   - Notificaciones masivas: Con reporte de errores")
            print("\n📧 Los reportes se envían a: ssasesoras430@gmail.com")
        else:
            print("\n❌ Configuración de correo incompleta")
            print("   Por favor, verifica la configuración SMTP en settings.py")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 