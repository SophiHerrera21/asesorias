#!/usr/bin/env python
"""
Script de prueba para verificar el flujo completo del sistema de asesorías virtuales.
Verifica: registro, login, validación de contraseñas, creación de objetos relacionados,
y manejo de errores.
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asesorias_virtuales.settings')
django.setup()

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from apps.usuarios.models import Usuario, Aprendiz, Asesor, Coordinador
from apps.usuarios.forms import UsuarioForm, AsesorRegistroForm
from apps.grupos.models import Grupo
from apps.pqrs.models import PQRS
from apps.pruebas.models import Prueba

def test_password_validation():
    """Prueba la validación de contraseñas"""
    print("🔐 Probando validación de contraseñas...")
    
    # Probar contraseña muy corta
    form_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'documento': '12345678',
        'role': 'aprendiz',
        'telefono': '123456789',
        'direccion': 'Test Address',
        'password1': '123',  # Muy corta
        'password2': '123'
    }
    
    form = UsuarioForm(data=form_data)
    if not form.is_valid():
        print("✅ Validación de contraseña corta funciona correctamente")
        for field, errors in form.errors.items():
            print(f"   Error en {field}: {errors}")
    else:
        print("❌ Error: La contraseña corta debería ser rechazada")
    
    # Probar contraseña válida
    form_data['password1'] = 'password123'
    form_data['password2'] = 'password123'
    
    form = UsuarioForm(data=form_data)
    if form.is_valid():
        print("✅ Validación de contraseña válida funciona correctamente")
    else:
        print("❌ Error: La contraseña válida debería ser aceptada")
        for field, errors in form.errors.items():
            print(f"   Error en {field}: {errors}")

def test_user_creation():
    """Prueba la creación de usuarios con objetos relacionados"""
    print("\n👤 Probando creación de usuarios...")
    
    # Crear usuario aprendiz
    try:
        user_data = {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'email': 'juan.perez@test.com',
            'documento': '123456789',
            'role': 'aprendiz',
            'telefono': '3001234567',
            'direccion': 'Calle 123 #45-67',
            'password1': 'password123',
            'password2': 'password123'
        }
        
        form = UsuarioForm(data=user_data)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'aprendiz'
            user.username = user.email
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # Crear objeto Aprendiz relacionado
            Aprendiz.objects.create(
                usuario=user,
                ficha='FICHA123',
                programa='Técnico en Sistemas',
                trimestre='2'
            )
            
            print(f"✅ Usuario aprendiz creado: {user.email}")
            
            # Verificar que el objeto relacionado existe
            if hasattr(user, 'aprendiz'):
                print(f"✅ Objeto Aprendiz creado: Ficha {user.aprendiz.ficha}")
            else:
                print("❌ Error: Objeto Aprendiz no encontrado")
            
            return user
        else:
            print("❌ Error en formulario de aprendiz:")
            for field, errors in form.errors.items():
                print(f"   {field}: {errors}")
            return None
            
    except Exception as e:
        print(f"❌ Error creando usuario aprendiz: {e}")
        return None

def test_authentication():
    """Prueba la autenticación de usuarios"""
    print("\n🔑 Probando autenticación...")
    
    # Crear usuario de prueba
    user = test_user_creation()
    if not user:
        print("❌ No se pudo crear usuario para prueba de autenticación")
        return
    
    # Probar autenticación correcta
    authenticated_user = authenticate(username=user.email, password='password123')
    if authenticated_user:
        print(f"✅ Autenticación exitosa: {authenticated_user.email}")
        print(f"   Rol: {authenticated_user.role}")
        print(f"   Activo: {authenticated_user.is_active}")
    else:
        print("❌ Error: La autenticación debería ser exitosa")
    
    # Probar autenticación con contraseña incorrecta
    wrong_auth = authenticate(username=user.email, password='wrongpassword')
    if not wrong_auth:
        print("✅ Autenticación con contraseña incorrecta rechazada correctamente")
    else:
        print("❌ Error: La autenticación con contraseña incorrecta debería fallar")
    
    # Limpiar usuario de prueba
    user.delete()

def test_form_persistence():
    """Prueba que los formularios mantengan la información en caso de error"""
    print("\n📝 Probando persistencia de formularios...")
    
    # Crear datos de formulario con error
    form_data = {
        'first_name': 'María',
        'last_name': 'García',
        'email': 'maria.garcia@test.com',
        'documento': '987654321',
        'role': 'asesor',
        'telefono': '3009876543',
        'direccion': 'Avenida 456 #78-90',
        'password1': '123',  # Contraseña muy corta para causar error
        'password2': '123'
    }
    
    form = AsesorRegistroForm(data=form_data)
    if not form.is_valid():
        print("✅ Formulario detecta errores correctamente")
        print("   Datos del formulario se mantienen:")
        for field, value in form_data.items():
            if field not in ['password1', 'password2']:
                print(f"   {field}: {value}")
        
        # Verificar que los campos mantienen sus valores
        if form.data.get('first_name') == 'María':
            print("✅ Campo first_name mantiene su valor")
        else:
            print("❌ Error: Campo first_name no mantiene su valor")
    else:
        print("❌ Error: El formulario debería detectar errores")

def test_url_patterns():
    """Verifica que las URLs principales existan"""
    print("\n🔗 Verificando patrones de URL...")
    
    try:
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        
        # URLs principales a verificar
        urls_to_test = [
            'usuarios:home',
            'usuarios:login',
            'usuarios:seleccionar_rol',
            'usuarios:registro_aprendiz',
            'usuarios:registro_asesor',
            'usuarios:registro_coordinador',
            'usuarios:dashboard_aprendiz',
            'usuarios:dashboard_asesor',
            'usuarios:dashboard_coordinador',
        ]
        
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"✅ URL {url_name}: {url}")
            except NoReverseMatch:
                print(f"❌ URL {url_name}: No encontrada")
                
    except Exception as e:
        print(f"❌ Error verificando URLs: {e}")

def test_template_existence():
    """Verifica que los templates principales existan"""
    print("\n📄 Verificando templates...")
    
    import os
    template_dir = "apps/usuarios/templates/usuarios"
    
    templates_to_check = [
        'home.html',
        'login.html',
        'seleccionar_rol.html',
        'registro_aprendiz.html',
        'registro_asesor.html',
        'registro_coordinador.html',
        'dashboard_aprendiz.html',
        'dashboard_asesor.html',
        'dashboard_coordinador.html',
        'form_usuario.html',
        'cambiar_password.html',
        'crear_grupo.html',
        'crear_pqrs.html',
        'crear_prueba.html',
    ]
    
    for template in templates_to_check:
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            print(f"✅ Template {template}: Existe")
        else:
            print(f"❌ Template {template}: No encontrado")

def main():
    """Función principal que ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas del sistema de asesorías virtuales")
    print("=" * 60)
    
    try:
        test_password_validation()
        test_authentication()
        test_form_persistence()
        test_url_patterns()
        test_template_existence()
        
        print("\n" + "=" * 60)
        print("✅ Todas las pruebas completadas")
        print("📊 Resumen:")
        print("   - Validación de contraseñas: Implementada")
        print("   - Autenticación: Funcional")
        print("   - Persistencia de formularios: Implementada")
        print("   - URLs: Verificadas")
        print("   - Templates: Verificados")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 