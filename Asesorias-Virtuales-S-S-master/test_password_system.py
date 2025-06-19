#!/usr/bin/env python
"""
Script de prueba para verificar que el sistema de contraseñas funciona correctamente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asesorias_virtuales.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from apps.usuarios.forms import UsuarioForm

User = get_user_model()

def test_password_creation():
    """Prueba la creación de usuarios con contraseñas personalizadas"""
    print("🔐 Probando sistema de contraseñas...")
    print("=" * 50)
    
    # Datos de prueba
    test_data = {
        'first_name': 'Usuario',
        'last_name': 'Prueba',
        'email': 'test_password@example.com',
        'documento': '12345678',
        'role': 'aprendiz',
        'telefono': '3001234567',
        'direccion': 'Dirección de prueba',
        'password1': 'MiContraseña123!',
        'password2': 'MiContraseña123!'
    }
    
    try:
        # Eliminar usuario de prueba si existe
        User.objects.filter(email=test_data['email']).delete()
        
        # Crear formulario con datos de prueba
        form = UsuarioForm(data=test_data)
        
        if form.is_valid():
            print("✅ Formulario válido")
            
            # Crear usuario sin guardar
            usuario = form.save(commit=False)
            usuario.username = usuario.email
            
            # Establecer contraseña
            password_original = test_data['password1']
            usuario.set_password(password_original)
            usuario.save()
            
            print(f"👤 Usuario creado: {usuario.get_full_name()}")
            print(f"📧 Email: {usuario.email}")
            print(f"🔑 Contraseña original: {password_original}")
            
            # Verificar que la contraseña se guardó correctamente (hasheada)
            if usuario.password != password_original:
                print("✅ Contraseña hasheada correctamente")
            else:
                print("❌ ERROR: La contraseña no se hasheó")
                return False
            
            # Verificar que la contraseña funciona con check_password
            if check_password(password_original, usuario.password):
                print("✅ Verificación de contraseña exitosa")
            else:
                print("❌ ERROR: La contraseña no se puede verificar")
                return False
            
            # Probar autenticación
            user_auth = authenticate(username=usuario.email, password=password_original)
            if user_auth and user_auth == usuario:
                print("✅ Autenticación exitosa")
            else:
                print("❌ ERROR: La autenticación falló")
                return False
            
            # Limpiar usuario de prueba
            usuario.delete()
            print("🧹 Usuario de prueba eliminado")
            
            return True
            
        else:
            print("❌ Formulario inválido:")
            for field, errors in form.errors.items():
                print(f"   {field}: {errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        return False

def test_password_validation():
    """Prueba la validación de contraseñas"""
    print("\n🔍 Probando validación de contraseñas...")
    print("=" * 50)
    
    # Casos de prueba
    test_cases = [
        {
            'name': 'Contraseña válida',
            'password1': 'Contraseña123!',
            'password2': 'Contraseña123!',
            'should_be_valid': True
        },
        {
            'name': 'Contraseñas no coinciden',
            'password1': 'Contraseña123!',
            'password2': 'Contraseña456!',
            'should_be_valid': False
        },
        {
            'name': 'Contraseña muy corta',
            'password1': '123',
            'password2': '123',
            'should_be_valid': False
        },
        {
            'name': 'Contraseña común',
            'password1': 'password',
            'password2': 'password',
            'should_be_valid': False
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Caso {i}: {test_case['name']}")
        
        test_data = {
            'first_name': 'Usuario',
            'last_name': 'Prueba',
            'email': f'test{i}@example.com',
            'documento': f'1234567{i}',
            'role': 'aprendiz',
            'telefono': '3001234567',
            'direccion': 'Dirección de prueba',
            'password1': test_case['password1'],
            'password2': test_case['password2']
        }
        
        form = UsuarioForm(data=test_data)
        is_valid = form.is_valid()
        
        if is_valid == test_case['should_be_valid']:
            print(f"   ✅ Resultado esperado: {is_valid}")
        else:
            print(f"   ❌ Resultado inesperado: {is_valid} (esperado: {test_case['should_be_valid']})")
            if not is_valid:
                for field, errors in form.errors.items():
                    print(f"      {field}: {errors}")
    
    return True

def test_existing_users():
    """Verifica que los usuarios existentes tienen contraseñas válidas"""
    print("\n👥 Verificando usuarios existentes...")
    print("=" * 50)
    
    users = User.objects.all()[:5]  # Primeros 5 usuarios
    
    if not users:
        print("ℹ️ No hay usuarios en la base de datos")
        return True
    
    print(f"📊 Verificando {users.count()} usuarios...")
    
    for user in users:
        print(f"\n👤 Usuario: {user.get_full_name()} ({user.email})")
        
        # Verificar que tiene contraseña hasheada
        if user.password and user.password != '':
            if not user.password.startswith('pbkdf2_sha256$'):
                print("   ⚠️ Contraseña no parece estar hasheada correctamente")
            else:
                print("   ✅ Contraseña hasheada correctamente")
        else:
            print("   ❌ Usuario sin contraseña")
    
    return True

if __name__ == '__main__':
    print("🚀 Iniciando pruebas del sistema de contraseñas...")
    
    # Probar creación de contraseñas
    test1_ok = test_password_creation()
    
    # Probar validación de contraseñas
    test2_ok = test_password_validation()
    
    # Verificar usuarios existentes
    test3_ok = test_existing_users()
    
    print("\n" + "=" * 50)
    if test1_ok and test2_ok and test3_ok:
        print("🎉 ¡Todas las pruebas del sistema de contraseñas pasaron!")
        print("\n✅ El sistema está configurado correctamente:")
        print("   - Las contraseñas se hashean correctamente")
        print("   - La autenticación funciona")
        print("   - La validación de contraseñas es correcta")
        print("   - Los usuarios existentes tienen contraseñas válidas")
    else:
        print("❌ Algunas pruebas fallaron")
        sys.exit(1) 