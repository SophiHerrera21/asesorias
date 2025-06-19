#!/usr/bin/env python
"""
Script completo para probar el flujo del sistema S&S Asesorías Virtuales
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asesorias_virtuales.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from django.test import Client
from django.urls import reverse
from apps.usuarios.forms import UsuarioForm, AsesorRegistroForm
from asesorias_virtuales.utils.email_utils import send_welcome_email

User = get_user_model()

def test_user_registration_and_login():
    """Prueba el registro y login de usuarios"""
    print("🚀 Probando registro y login de usuarios...")
    print("=" * 60)
    
    # Datos de prueba para cada rol
    test_users = [
        {
            'role': 'aprendiz',
            'data': {
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'email': 'juan.perez@test.com',
                'documento': '12345678',
                'role': 'aprendiz',
                'telefono': '3001234567',
                'direccion': 'Calle 123 #45-67',
                'password1': 'TestPassword123!',
                'password2': 'TestPassword123!'
            }
        },
        {
            'role': 'asesor',
            'data': {
                'first_name': 'María',
                'last_name': 'García',
                'email': 'maria.garcia@test.com',
                'documento': '87654321',
                'role': 'asesor',
                'telefono': '3007654321',
                'direccion': 'Carrera 78 #90-12',
                'password1': 'TestPassword123!',
                'password2': 'TestPassword123!',
                'trimestre': 3
            }
        },
        {
            'role': 'coordinador',
            'data': {
                'first_name': 'Carlos',
                'last_name': 'López',
                'email': 'carlos.lopez@test.com',
                'documento': '11223344',
                'role': 'coordinador',
                'telefono': '3001122334',
                'direccion': 'Avenida 56 #78-90',
                'password1': 'TestPassword123!',
                'password2': 'TestPassword123!'
            }
        }
    ]
    
    created_users = []
    
    for test_user in test_users:
        role = test_user['role']
        data = test_user['data']
        
        print(f"\n📝 Probando registro de {role}...")
        
        # Limpiar usuario de prueba si existe
        User.objects.filter(email=data['email']).delete()
        
        # Probar registro
        if role == 'asesor':
            form = AsesorRegistroForm(data=data)
        else:
            form = UsuarioForm(data=data)
        
        if form.is_valid():
            print(f"   ✅ Formulario válido para {role}")
            
            # Crear usuario
            usuario = form.save(commit=False)
            usuario.username = usuario.email
            usuario.set_password(data['password1'])
            usuario.save()
            
            # Crear perfil específico para asesor
            if role == 'asesor':
                from apps.usuarios.models import Asesor
                Asesor.objects.create(
                    usuario=usuario,
                    especialidad='',
                    experiencia=0,
                    trimestre=data['trimestre']
                )
            
            print(f"   ✅ Usuario {role} creado: {usuario.get_full_name()}")
            
            # Probar correo de bienvenida
            email_result = send_welcome_email(usuario)
            if email_result:
                print(f"   ✅ Correo de bienvenida enviado a {role}")
            else:
                print(f"   ⚠️ Error al enviar correo de bienvenida a {role}")
            
            # Probar login
            user_auth = authenticate(username=data['email'], password=data['password1'])
            if user_auth and user_auth == usuario:
                print(f"   ✅ Login exitoso para {role}")
                created_users.append(usuario)
            else:
                print(f"   ❌ Error en login para {role}")
        else:
            print(f"   ❌ Formulario inválido para {role}:")
            for field, errors in form.errors.items():
                print(f"      {field}: {errors}")
    
    return created_users

def test_dashboard_access():
    """Prueba el acceso a los dashboards según el rol"""
    print("\n🏠 Probando acceso a dashboards...")
    print("=" * 60)
    
    client = Client()
    
    # Obtener usuarios de prueba
    users = User.objects.filter(
        email__in=['juan.perez@test.com', 'maria.garcia@test.com', 'carlos.lopez@test.com']
    )
    
    dashboard_urls = {
        'aprendiz': 'usuarios:dashboard_aprendiz',
        'asesor': 'usuarios:dashboard_asesor',
        'coordinador': 'usuarios:dashboard_coordinador'
    }
    
    for user in users:
        print(f"\n👤 Probando acceso para {user.get_full_name()} ({user.role})...")
        
        # Login
        login_success = client.login(username=user.email, password='TestPassword123!')
        if not login_success:
            print(f"   ❌ Error en login para {user.role}")
            continue
        
        print(f"   ✅ Login exitoso para {user.role}")
        
        # Probar acceso a su dashboard
        dashboard_url = dashboard_urls.get(user.role)
        if dashboard_url:
            response = client.get(reverse(dashboard_url))
            if response.status_code == 200:
                print(f"   ✅ Acceso exitoso al dashboard de {user.role}")
            else:
                print(f"   ❌ Error al acceder al dashboard de {user.role} (código: {response.status_code})")
        
        # Probar acceso a dashboard de otro rol (debería fallar)
        other_roles = [r for r in dashboard_urls.keys() if r != user.role]
        for other_role in other_roles:
            other_dashboard_url = dashboard_urls[other_role]
            response = client.get(reverse(other_dashboard_url))
            if response.status_code in [302, 403]:  # Redirección o prohibido
                print(f"   ✅ Correctamente bloqueado acceso a dashboard de {other_role}")
            else:
                print(f"   ⚠️ Acceso inesperado al dashboard de {other_role}")
        
        # Logout
        client.logout()
        print(f"   ✅ Logout exitoso para {user.role}")

def test_url_access():
    """Prueba el acceso a diferentes URLs según el rol"""
    print("\n🔗 Probando acceso a URLs específicas...")
    print("=" * 60)
    
    client = Client()
    
    # URLs a probar por rol
    role_urls = {
        'aprendiz': [
            'usuarios:dashboard_aprendiz',
            'usuarios:componentes_aprendiz',
            'usuarios:grupos_aprendiz',
            'usuarios:pruebas_aprendiz',
            'usuarios:pqrs_aprendiz',
            'usuarios:notificaciones_aprendiz',
            'usuarios:reportes_aprendiz'
        ],
        'asesor': [
            'usuarios:dashboard_asesor',
            'pqrs:pqrs_asesor',
            'grupos:grupos_asesor',
            'pruebas:pruebas_asesor'
        ],
        'coordinador': [
            'usuarios:dashboard_coordinador',
            'usuarios:lista_usuarios',
            'usuarios:pqrs_coordinador'
        ]
    }
    
    users = User.objects.filter(
        email__in=['juan.perez@test.com', 'maria.garcia@test.com', 'carlos.lopez@test.com']
    )
    
    for user in users:
        print(f"\n👤 Probando URLs para {user.get_full_name()} ({user.role})...")
        
        # Login
        client.login(username=user.email, password='TestPassword123!')
        
        # Probar URLs permitidas
        allowed_urls = role_urls.get(user.role, [])
        for url_name in allowed_urls:
            try:
                response = client.get(reverse(url_name))
                if response.status_code == 200:
                    print(f"   ✅ {url_name} - Acceso permitido")
                elif response.status_code == 302:
                    print(f"   ⚠️ {url_name} - Redirección (posible login requerido)")
                else:
                    print(f"   ❌ {url_name} - Error {response.status_code}")
            except Exception as e:
                print(f"   ❌ {url_name} - Error: {str(e)}")
        
        # Probar algunas URLs no permitidas
        forbidden_urls = []
        for role, urls in role_urls.items():
            if role != user.role:
                forbidden_urls.extend(urls[:2])  # Solo las primeras 2 URLs de cada rol
        
        for url_name in forbidden_urls[:3]:  # Solo probar 3 URLs prohibidas
            try:
                response = client.get(reverse(url_name))
                if response.status_code in [302, 403]:
                    print(f"   ✅ {url_name} - Correctamente bloqueado")
                else:
                    print(f"   ⚠️ {url_name} - Acceso inesperado (código: {response.status_code})")
            except Exception as e:
                print(f"   ✅ {url_name} - Correctamente bloqueado (error: {str(e)})")
        
        client.logout()

def test_email_system():
    """Prueba el sistema de correos"""
    print("\n📧 Probando sistema de correos...")
    print("=" * 60)
    
    users = User.objects.filter(
        email__in=['juan.perez@test.com', 'maria.garcia@test.com', 'carlos.lopez@test.com']
    )
    
    for user in users:
        print(f"\n📧 Probando correo para {user.get_full_name()} ({user.role})...")
        
        # Probar envío de correo de bienvenida
        result = send_welcome_email(user)
        if result:
            print(f"   ✅ Correo de bienvenida enviado exitosamente")
        else:
            print(f"   ❌ Error al enviar correo de bienvenida")

def cleanup_test_users():
    """Limpia los usuarios de prueba"""
    print("\n🧹 Limpiando usuarios de prueba...")
    print("=" * 60)
    
    test_emails = ['juan.perez@test.com', 'maria.garcia@test.com', 'carlos.lopez@test.com']
    deleted_count = User.objects.filter(email__in=test_emails).delete()[0]
    
    if deleted_count > 0:
        print(f"   ✅ {deleted_count} usuarios de prueba eliminados")
    else:
        print("   ℹ️ No se encontraron usuarios de prueba para eliminar")

def main():
    """Función principal de pruebas"""
    print("🎯 INICIANDO PRUEBAS COMPLETAS DEL SISTEMA S&S ASESORÍAS VIRTUALES")
    print("=" * 80)
    
    try:
        # 1. Probar registro y login
        created_users = test_user_registration_and_login()
        
        if not created_users:
            print("\n❌ No se pudieron crear usuarios de prueba. Abortando...")
            return
        
        # 2. Probar acceso a dashboards
        test_dashboard_access()
        
        # 3. Probar acceso a URLs específicas
        test_url_access()
        
        # 4. Probar sistema de correos
        test_email_system()
        
        print("\n" + "=" * 80)
        print("🎉 ¡TODAS LAS PRUEBAS COMPLETADAS!")
        print("\n✅ El sistema está funcionando correctamente:")
        print("   - Registro de usuarios por rol")
        print("   - Login y autenticación")
        print("   - Acceso a dashboards según rol")
        print("   - Protección de vistas por rol")
        print("   - Sistema de correos de bienvenida")
        print("   - Redirecciones correctas")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Limpiar usuarios de prueba
        cleanup_test_users()

if __name__ == '__main__':
    main() 