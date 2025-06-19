#!/usr/bin/env python
"""
Script para probar que la contraseña ingresada en el registro es la que permite iniciar sesión.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asesorias_virtuales.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from apps.usuarios.forms import UsuarioForm

User = get_user_model()

def test_password_registration():
    print('--- Prueba de registro y login con contraseña personalizada ---')
    email = 'prueba.password@test.com'
    password = 'MiClaveSuperSecreta123!'
    test_data = {
        'first_name': 'Test',
        'last_name': 'Password',
        'email': email,
        'documento': '99999999',
        'role': 'aprendiz',
        'telefono': '3000000000',
        'direccion': 'Calle Falsa 123',
        'password1': password,
        'password2': password
    }
    # Eliminar usuario previo
    User.objects.filter(email=email).delete()
    # Registrar usuario
    form = UsuarioForm(data=test_data)
    if not form.is_valid():
        print('❌ El formulario de registro no es válido:')
        for field, errors in form.errors.items():
            print(f'   {field}: {errors}')
        sys.exit(1)
    usuario = form.save(commit=False)
    usuario.username = usuario.email
    usuario.set_password(password)
    usuario.save()
    print('✅ Usuario registrado correctamente.')
    # Intentar login
    user_auth = authenticate(username=email, password=password)
    if user_auth and user_auth.email == email:
        print('✅ Login exitoso con la contraseña ingresada.')
        # Limpiar usuario de prueba
        user_auth.delete()
        print('🧹 Usuario de prueba eliminado.')
        sys.exit(0)
    else:
        print('❌ ERROR: No se pudo iniciar sesión con la contraseña ingresada.')
        sys.exit(2)

if __name__ == '__main__':
    test_password_registration() 