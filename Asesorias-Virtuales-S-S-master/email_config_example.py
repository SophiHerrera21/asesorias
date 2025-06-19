"""
Ejemplo de configuración de email para S&S Asesorías Virtuales

Este archivo muestra cómo configurar el sistema de correos de bienvenida.
Copia estas configuraciones a tu archivo settings.py
"""

# =============================================================================
# CONFIGURACIÓN DE EMAIL - GMAIL
# =============================================================================

# Configuración básica de SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Credenciales de Gmail
EMAIL_HOST_USER = 'tu-email@gmail.com'  # Cambiar por tu email
EMAIL_HOST_PASSWORD = 'tu-contraseña-de-aplicacion'  # Cambiar por tu contraseña de aplicación
DEFAULT_FROM_EMAIL = 'S&S Asesorías Virtuales <tu-email@gmail.com>'

# Configuraciones adicionales
EMAIL_TIMEOUT = 20
EMAIL_FAIL_SILENTLY = False

# Configuración del sitio
SITE_URL = 'http://localhost:8000'  # Cambiar en producción
SITE_NAME = 'S&S Asesorías Virtuales'

# =============================================================================
# INSTRUCCIONES PARA CONFIGURAR GMAIL
# =============================================================================

"""
PASOS PARA CONFIGURAR GMAIL:

1. HABILITAR AUTENTICACIÓN DE 2 FACTORES:
   - Ve a tu cuenta de Google
   - Seguridad > Verificación en 2 pasos
   - Activa la verificación en 2 pasos

2. GENERAR CONTRASEÑA DE APLICACIÓN:
   - Ve a Seguridad > Contraseñas de aplicación
   - Selecciona "Otra" y dale un nombre (ej: "Django S&S")
   - Copia la contraseña generada (16 caracteres)

3. CONFIGURAR EN SETTINGS.PY:
   - Reemplaza EMAIL_HOST_USER con tu email
   - Reemplaza EMAIL_HOST_PASSWORD con la contraseña de aplicación
   - Actualiza DEFAULT_FROM_EMAIL con tu email

4. PROBAR LA CONFIGURACIÓN:
   python manage.py test_welcome_email
"""

# =============================================================================
# CONFIGURACIÓN ALTERNATIVA - OUTLOOK/HOTMAIL
# =============================================================================

"""
# Para usar Outlook/Hotmail:
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@outlook.com'
EMAIL_HOST_PASSWORD = 'tu-contraseña'
"""

# =============================================================================
# CONFIGURACIÓN ALTERNATIVA - YAHOO
# =============================================================================

"""
# Para usar Yahoo:
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@yahoo.com'
EMAIL_HOST_PASSWORD = 'tu-contraseña-de-aplicacion'
"""

# =============================================================================
# CONFIGURACIÓN PARA DESARROLLO (CONSOLA)
# =============================================================================

"""
# Para desarrollo local (emails en consola):
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Esto mostrará los emails en la consola en lugar de enviarlos
# Útil para desarrollo y pruebas
"""

# =============================================================================
# CONFIGURACIÓN PARA PRODUCCIÓN
# =============================================================================

"""
# Para producción, considera usar servicios como:
# - SendGrid
# - Mailgun
# - Amazon SES
# - Postmark

# Ejemplo con SendGrid:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'tu-api-key-de-sendgrid'
"""

# =============================================================================
# VERIFICACIÓN DE CONFIGURACIÓN
# =============================================================================

def verify_email_config():
    """
    Función para verificar que la configuración de email esté correcta
    """
    required_settings = [
        'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_HOST_USER', 
        'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL'
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not globals().get(setting):
            missing_settings.append(setting)
    
    if missing_settings:
        print(f"❌ Configuraciones faltantes: {', '.join(missing_settings)}")
        return False
    else:
        print("✅ Configuración de email completa")
        return True

if __name__ == '__main__':
    print("🔧 Verificando configuración de email...")
    verify_email_config() 