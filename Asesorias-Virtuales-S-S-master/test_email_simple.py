#!/usr/bin/env python
"""
Script simple para probar el envío de correo con la nueva contraseña.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asesorias_virtuales.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_simple_email():
    """Prueba envío simple de correo"""
    print("📧 Probando envío simple de correo...")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD[:4]}...{settings.EMAIL_HOST_PASSWORD[-4:]}")
    
    try:
        result = send_mail(
            subject='Prueba de correo - S&S Asesorías',
            message='Este es un correo de prueba para verificar que la configuración SMTP funciona correctamente.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['ssasesoras430@gmail.com'],
            fail_silently=False,
        )
        
        if result:
            print("✅ Correo enviado exitosamente!")
            return True
        else:
            print("❌ Error: No se pudo enviar el correo")
            return False
            
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")
        return False

def test_welcome_email():
    """Prueba envío de correo de bienvenida"""
    print("\n🎉 Probando correo de bienvenida...")
    
    try:
        from asesorias_virtuales.utils.email_utils import send_welcome_email
        
        # Crear un usuario de prueba
        from apps.usuarios.models import Usuario
        test_user = Usuario(
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
        result = send_welcome_email(test_user)
        
        if result:
            print("✅ Correo de bienvenida enviado exitosamente!")
            return True
        else:
            print("❌ Error: No se pudo enviar el correo de bienvenida")
            return False
            
    except Exception as e:
        print(f"❌ Error al enviar correo de bienvenida: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de correo simple")
    print("=" * 50)
    
    # Probar envío simple
    simple_ok = test_simple_email()
    
    # Probar correo de bienvenida
    welcome_ok = test_welcome_email()
    
    print("\n" + "=" * 50)
    if simple_ok and welcome_ok:
        print("✅ Todas las pruebas de correo exitosas!")
    else:
        print("❌ Algunas pruebas fallaron")
        print("\n💡 Sugerencias:")
        print("1. Verifica que la autenticación de 2 factores esté habilitada en Gmail")
        print("2. Genera una nueva contraseña de aplicación")
        print("3. Asegúrate de que la contraseña no tenga espacios")
        print("4. Espera unos minutos para que la contraseña se active")

if __name__ == "__main__":
    main() 