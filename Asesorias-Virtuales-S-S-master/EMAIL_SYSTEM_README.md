# Sistema de Correos de Bienvenida - S&S Asesorías Virtuales

## 📧 Descripción

El sistema de correos de bienvenida se encarga de enviar emails automáticos a los usuarios cuando se registran en la plataforma. El sistema está diseñado para usar la contraseña que el usuario ingresa durante el registro, no contraseñas generadas automáticamente.

## 🚀 Características

### ✅ Funcionalidades Implementadas

1. **Correo de Bienvenida Personalizado**
   - Email HTML responsivo y profesional
   - Información específica según el rol del usuario
   - Credenciales de acceso claras
   - Recomendaciones de seguridad

2. **Uso de Contraseña del Usuario**
   - El sistema utiliza la contraseña que el usuario ingresa
   - No se generan contraseñas automáticamente
   - El email indica que la contraseña es la ingresada durante el registro

3. **Configuración Robusta**
   - Configuración SMTP para Gmail
   - Manejo de errores y logging
   - Timeouts configurados
   - Fallback para errores de envío

## 📁 Estructura de Archivos

```
asesorias_virtuales/
├── templates/
│   └── emails/
│       └── welcome.html          # Template del correo de bienvenida
├── utils/
│   └── email_utils.py           # Funciones de envío de emails
└── settings.py                  # Configuración de email

test_email.py                    # Script de prueba del sistema
```

## ⚙️ Configuración

### Configuración de Email (settings.py)

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ssasesoras430@gmail.com'
EMAIL_HOST_PASSWORD = 'ekjmybttzeylvpqs'
DEFAULT_FROM_EMAIL = 'S&S Asesoras Virtuales <ssasesoras430@gmail.com>'

# Additional email settings
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 20
EMAIL_FAIL_SILENTLY = False

# Site configuration
SITE_URL = 'http://localhost:8000'  # Cambiar en producción
SITE_NAME = 'S&S Asesorías Virtuales'
```

### Configuración de Gmail

Para usar Gmail como servidor SMTP:

1. Habilitar autenticación de 2 factores en la cuenta de Gmail
2. Generar una contraseña de aplicación
3. Usar esa contraseña en `EMAIL_HOST_PASSWORD`

## 🔧 Uso

### Envío Automático

El correo de bienvenida se envía automáticamente cuando un usuario se registra:

```python
# En las vistas de registro (views.py)
from asesorias_virtuales.utils.email_utils import send_welcome_email

def registro_aprendiz(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.role = 'aprendiz'
            usuario.username = usuario.email
            usuario.set_password(form.cleaned_data['password1'])  # Usa la contraseña del usuario
            usuario.save()
            
            # Enviar correo de bienvenida
            send_welcome_email(usuario)
            
            messages.success(request, 'Registro exitoso. Se ha enviado un correo de bienvenida.')
            return redirect('usuarios:login')
```

### Envío Manual

```python
from asesorias_virtuales.utils.email_utils import send_welcome_email

# Enviar correo de bienvenida a un usuario
result = send_welcome_email(user)

if result:
    print("Correo enviado exitosamente")
else:
    print("Error al enviar el correo")
```

## 📧 Template del Correo

El template `welcome.html` incluye:

- **Header profesional** con logo y branding
- **Mensaje personalizado** con el nombre del usuario
- **Credenciales de acceso** (email y contraseña)
- **Funcionalidades específicas** según el rol
- **Botón de acceso** directo a la plataforma
- **Recomendaciones de seguridad**
- **Footer** con información de contacto

### Características del Template

- ✅ Diseño responsivo
- ✅ Compatible con clientes de email
- ✅ Colores corporativos
- ✅ Iconos y emojis para mejor UX
- ✅ Información específica por rol

## 🧪 Pruebas

### Script de Prueba

Ejecutar el script de prueba para verificar el sistema:

```bash
python test_email.py
```

El script verifica:
- Configuración de email
- Envío de correo de prueba
- Manejo de errores

### Pruebas Manuales

1. **Registrar un nuevo usuario**
2. **Verificar que se reciba el correo**
3. **Comprobar que la contraseña sea la ingresada**
4. **Verificar el diseño en diferentes clientes de email**

## 🔒 Seguridad

### Recomendaciones Implementadas

- ✅ No se envían contraseñas en texto plano
- ✅ Se indica que la contraseña es la ingresada por el usuario
- ✅ Recomendaciones de seguridad en el email
- ✅ Timeouts configurados para evitar bloqueos
- ✅ Logging de errores para monitoreo

### Configuraciones de Seguridad

```python
EMAIL_USE_TLS = True          # Encriptación TLS
EMAIL_TIMEOUT = 20           # Timeout de 20 segundos
EMAIL_FAIL_SILENTLY = False  # Mostrar errores para debugging
```

## 🐛 Solución de Problemas

### Errores Comunes

1. **Error de autenticación SMTP**
   - Verificar credenciales de Gmail
   - Asegurar que la autenticación de 2 factores esté habilitada
   - Usar contraseña de aplicación, no la contraseña principal

2. **Correo no se envía**
   - Verificar configuración de firewall
   - Comprobar que el puerto 587 esté abierto
   - Revisar logs de Django

3. **Correo llega a spam**
   - Configurar SPF y DKIM en el dominio
   - Usar un dominio verificado
   - Evitar palabras que activen filtros de spam

### Logs y Debugging

```python
import logging
logger = logging.getLogger(__name__)

# Los logs se guardan automáticamente
logger.info("Correo enviado exitosamente")
logger.error("Error al enviar correo: {error}")
```

## 📈 Monitoreo

### Métricas a Monitorear

- Tasa de envío exitoso
- Tiempo de entrega
- Tasa de apertura (si se implementa tracking)
- Errores de envío

### Logs Importantes

- Envío exitoso: `Welcome email sent successfully to {email}`
- Error de envío: `Error sending welcome email to {email}: {error}`
- Configuración: Verificar settings en startup

## 🔄 Actualizaciones Futuras

### Mejoras Planificadas

- [ ] Tracking de apertura de emails
- [ ] Plantillas personalizables por rol
- [ ] Sistema de cola para envío masivo
- [ ] Integración con servicios de email transaccional
- [ ] A/B testing de templates

### Configuraciones Adicionales

- [ ] Configuración por entorno (dev/prod)
- [ ] Rate limiting para evitar spam
- [ ] Retry automático en caso de fallo
- [ ] Métricas de rendimiento

## 📞 Soporte

Para problemas con el sistema de correos:

1. Revisar logs de Django
2. Ejecutar script de prueba
3. Verificar configuración SMTP
4. Comprobar conectividad de red

---

**Nota**: Este sistema está diseñado para usar la contraseña que el usuario ingresa durante el registro, no contraseñas generadas automáticamente por el sistema. 