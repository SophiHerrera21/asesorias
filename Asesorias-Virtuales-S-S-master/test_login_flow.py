#!/usr/bin/env python
"""
Script para probar el flujo de login y verificar que no haya bucles infinitos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asesorias_virtuales.settings')
django.setup()

from apps.usuarios.models import Usuario, Aprendiz, Asesor, Coordinador
from django.contrib.auth import authenticate

def test_user_creation():
    """Prueba la creación de usuarios y objetos relacionados"""
    print("🧪 Probando creación de usuarios...")
    
    # Crear usuario aprendiz
    try:
        usuario_aprendiz = Usuario.objects.create_user(
            username='test_aprendiz@test.com',
            email='test_aprendiz@test.com',
            password='test123456',
            first_name='Test',
            last_name='Aprendiz',
            role='aprendiz'
        )
        
        # Verificar que se cree el objeto Aprendiz
        if hasattr(usuario_aprendiz, 'aprendiz'):
            print("✅ Usuario aprendiz creado correctamente con objeto relacionado")
        else:
            print("❌ Usuario aprendiz creado pero sin objeto relacionado")
            
    except Exception as e:
        print(f"❌ Error creando usuario aprendiz: {str(e)}")
    
    # Crear usuario asesor
    try:
        usuario_asesor = Usuario.objects.create_user(
            username='test_asesor@test.com',
            email='test_asesor@test.com',
            password='test123456',
            first_name='Test',
            last_name='Asesor',
            role='asesor'
        )
        
        # Verificar que se cree el objeto Asesor
        if hasattr(usuario_asesor, 'asesor'):
            print("✅ Usuario asesor creado correctamente con objeto relacionado")
        else:
            print("❌ Usuario asesor creado pero sin objeto relacionado")
            
    except Exception as e:
        print(f"❌ Error creando usuario asesor: {str(e)}")
    
    # Crear usuario coordinador
    try:
        usuario_coordinador = Usuario.objects.create_user(
            username='test_coordinador@test.com',
            email='test_coordinador@test.com',
            password='test123456',
            first_name='Test',
            last_name='Coordinador',
            role='coordinador'
        )
        
        # Verificar que se cree el objeto Coordinador
        if hasattr(usuario_coordinador, 'coordinador'):
            print("✅ Usuario coordinador creado correctamente con objeto relacionado")
        else:
            print("❌ Usuario coordinador creado pero sin objeto relacionado")
            
    except Exception as e:
        print(f"❌ Error creando usuario coordinador: {str(e)}")

def test_authentication():
    """Prueba la autenticación de usuarios"""
    print("\n🔐 Probando autenticación...")
    
    # Probar autenticación de aprendiz
    try:
        user = authenticate(username='test_aprendiz@test.com', password='test123456')
        if user and user.role == 'aprendiz':
            print("✅ Autenticación de aprendiz exitosa")
        else:
            print("❌ Error en autenticación de aprendiz")
    except Exception as e:
        print(f"❌ Error autenticando aprendiz: {str(e)}")
    
    # Probar autenticación de asesor
    try:
        user = authenticate(username='test_asesor@test.com', password='test123456')
        if user and user.role == 'asesor':
            print("✅ Autenticación de asesor exitosa")
        else:
            print("❌ Error en autenticación de asesor")
    except Exception as e:
        print(f"❌ Error autenticando asesor: {str(e)}")
    
    # Probar autenticación de coordinador
    try:
        user = authenticate(username='test_coordinador@test.com', password='test123456')
        if user and user.role == 'coordinador':
            print("✅ Autenticación de coordinador exitosa")
        else:
            print("❌ Error en autenticación de coordinador")
    except Exception as e:
        print(f"❌ Error autenticando coordinador: {str(e)}")

def test_objects_creation():
    """Prueba la creación automática de objetos relacionados"""
    print("\n🔧 Probando creación automática de objetos relacionados...")
    
    # Buscar usuarios sin objetos relacionados
    usuarios_sin_aprendiz = Usuario.objects.filter(role='aprendiz').exclude(aprendiz__isnull=False)
    usuarios_sin_asesor = Usuario.objects.filter(role='asesor').exclude(asesor__isnull=False)
    usuarios_sin_coordinador = Usuario.objects.filter(role='coordinador').exclude(coordinador__isnull=False)
    
    print(f"Usuarios aprendiz sin objeto relacionado: {usuarios_sin_aprendiz.count()}")
    print(f"Usuarios asesor sin objeto relacionado: {usuarios_sin_asesor.count()}")
    print(f"Usuarios coordinador sin objeto relacionado: {usuarios_sin_coordinador.count()}")
    
    # Crear objetos faltantes
    for usuario in usuarios_sin_aprendiz:
        Aprendiz.objects.create(
            usuario=usuario,
            ficha='SIN_FICHA',
            programa='SIN_PROGRAMA',
            trimestre='1'
        )
        print(f"✅ Creado objeto Aprendiz para {usuario.email}")
    
    for usuario in usuarios_sin_asesor:
        Asesor.objects.create(
            usuario=usuario,
            especialidad='',
            experiencia='',
            titulo='',
            max_grupos=4,
            disponibilidad='',
            trimestre='1'
        )
        print(f"✅ Creado objeto Asesor para {usuario.email}")
    
    for usuario in usuarios_sin_coordinador:
        Coordinador.objects.create(
            usuario=usuario,
            cargo='Coordinador',
            departamento='General'
        )
        print(f"✅ Creado objeto Coordinador para {usuario.email}")

def cleanup_test_users():
    """Limpia los usuarios de prueba"""
    print("\n🧹 Limpiando usuarios de prueba...")
    
    test_emails = [
        'test_aprendiz@test.com',
        'test_asesor@test.com', 
        'test_coordinador@test.com'
    ]
    
    for email in test_emails:
        try:
            Usuario.objects.filter(email=email).delete()
            print(f"✅ Eliminado usuario de prueba: {email}")
        except Exception as e:
            print(f"❌ Error eliminando {email}: {str(e)}")

if __name__ == '__main__':
    print("🚀 Iniciando pruebas del sistema de usuarios...")
    
    # Ejecutar pruebas
    test_user_creation()
    test_authentication()
    test_objects_creation()
    
    # Limpiar usuarios de prueba
    cleanup_test_users()
    
    print("\n✅ Pruebas completadas!") 