# S&S - Sistema de Asesorías Virtuales

Sistema de gestión de asesorías virtuales para aprendices SENA.

## Características Principales

- Gestión de usuarios (Aprendices, Asesores y Coordinadores)
- Sistema de componentes/materias
- Gestión de grupos y asesorías
- Sistema de pruebas y evaluaciones
- Sistema de PQRS
- **Sistema de correos de bienvenida automático**
- Notificaciones por correo electrónico
- Gestión de perfiles y documentos

## 🚀 Nuevas Funcionalidades

### Sistema de Correos de Bienvenida

El sistema ahora incluye un **sistema de correos de bienvenida automático** que:

- ✅ **Envía emails automáticos** cuando un usuario se registra
- ✅ **Usa la contraseña del usuario** (no genera contraseñas automáticamente)
- ✅ **Diseño profesional y responsivo** con información específica por rol
- ✅ **Configuración robusta** con manejo de errores y logging
- ✅ **Templates personalizables** según el tipo de usuario

#### Características del Sistema de Correos:

- 📧 **Email HTML responsivo** con diseño moderno
- 🎯 **Información específica** según el rol (Aprendiz, Asesor, Coordinador)
- 🔐 **Credenciales claras** sin exponer contraseñas
- 🛡️ **Recomendaciones de seguridad** incluidas
- 📱 **Compatible con móviles** y diferentes clientes de email

#### Configuración Rápida:

1. **Configurar Gmail** (ver `email_config_example.py`)
2. **Probar el sistema**: `python manage.py test_welcome_email`
3. **Documentación completa**: Ver `EMAIL_SYSTEM_README.md`

## Requisitos

- Python 3.8+
- MySQL 8.0+
- Virtualenv (recomendado)
- **Configuración de email SMTP** (Gmail recomendado)

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
- Crear archivo `.env` basado en `.env.example`
- Configurar credenciales de base de datos y correo

5. **Configurar sistema de correos**:
```bash
# Ver ejemplo de configuración
cat email_config_example.py

# Probar el sistema de correos
python manage.py test_welcome_email
```

6. Realizar migraciones:
```bash
python manage.py migrate
```

7. Crear superusuario:
```bash
python manage.py createsuperuser
```

8. Iniciar el servidor:
```bash
python manage.py runserver
```

## 📧 Sistema de Correos

### Configuración

El sistema de correos está configurado para usar Gmail SMTP. Para configurarlo:

1. **Habilitar autenticación de 2 factores** en tu cuenta de Gmail
2. **Generar contraseña de aplicación** en Google
3. **Actualizar settings.py** con tus credenciales
4. **Probar la configuración** con el comando de prueba

### Comandos Útiles

```bash
# Probar sistema de correos
python manage.py test_welcome_email

# Probar con email específico
python manage.py test_welcome_email --email usuario@ejemplo.com

# Probar con información detallada
python manage.py test_welcome_email --verbose
```

### Documentación

- 📖 **Documentación completa**: `EMAIL_SYSTEM_README.md`
- ⚙️ **Ejemplo de configuración**: `email_config_example.py`
- 🧪 **Script de prueba**: `test_email.py`

## Estructura del Proyecto

- `core/` - Aplicación principal
- `users/` - Gestión de usuarios
- `asesorias/` - Gestión de asesorías
- `grupos/` - Gestión de grupos
- `pruebas/` - Sistema de pruebas
- `pqrs/` - Sistema de PQRS
- `asesorias_virtuales/templates/emails/` - **Templates de correos**
- `asesorias_virtuales/utils/email_utils.py` - **Funciones de email**

## 🔧 Comandos de Gestión

```bash
# Probar sistema de correos
python manage.py test_welcome_email

# Crear superusuario
python manage.py createsuperuser

# Ejecutar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic
```

## 📞 Soporte

Para problemas con el sistema de correos:

1. Revisar `EMAIL_SYSTEM_README.md`
2. Ejecutar `python manage.py test_welcome_email`
3. Verificar configuración en `email_config_example.py`
4. Revisar logs de Django

## Licencia

Este proyecto es propiedad del SENA. 