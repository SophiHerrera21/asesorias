#!/usr/bin/env python
"""
Test automático para verificar el acceso a todas las vistas de usuarios según el rol.
"""
import os
import sys
import django
from django.test import Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asesorias_virtuales.settings')
django.setup()

User = get_user_model()

# Rutas a testear (nombre de url, kwargs si aplica, método)
ROUTES = [
    # (name, kwargs, method)
    ('usuarios:home', None, 'get'),
    ('usuarios:login', None, 'get'),
    ('usuarios:dashboard_aprendiz', None, 'get'),
    ('usuarios:dashboard_asesor', None, 'get'),
    ('usuarios:dashboard_coordinador', None, 'get'),
    ('usuarios:perfil_aprendiz', None, 'get'),
    ('usuarios:perfil_asesor', None, 'get'),
    ('usuarios:perfil_coordinador', None, 'get'),
    ('usuarios:configuracion_coordinador', None, 'get'),
    ('usuarios:entrada_unica_coordinador', None, 'get'),
    ('usuarios:reportes_coordinador', None, 'get'),
]

# Crear usuarios de prueba para cada rol
from apps.usuarios.models import Usuario, Aprendiz, Asesor, Coordinador

def get_or_create_user(email, role):
    user, created = Usuario.objects.get_or_create(email=email, defaults={
        'username': email,
        'role': role,
        'is_active': True,
        'password': 'pbkdf2_sha256$260000$test$test',
    })
    if role == 'aprendiz' and not hasattr(user, 'aprendiz'):
        Aprendiz.objects.get_or_create(usuario=user)
    if role == 'asesor' and not hasattr(user, 'asesor'):
        Asesor.objects.get_or_create(usuario=user)
    if role == 'coordinador' and not hasattr(user, 'coordinador'):
        Coordinador.objects.get_or_create(usuario=user)
    return user

def login_as(client, user):
    user.set_password('test12345')
    user.save()
    client.login(username=user.email, password='test12345')

def test_routes():
    client = Client()
    roles = ['anonimo', 'aprendiz', 'asesor', 'coordinador']
    users = {
        'aprendiz': get_or_create_user('aprendiz@test.com', 'aprendiz'),
        'asesor': get_or_create_user('asesor@test.com', 'asesor'),
        'coordinador': get_or_create_user('coordinador@test.com', 'coordinador'),
    }
    results = []
    for name, kwargs, method in ROUTES:
        for role in roles:
            client.logout()
            if role != 'anonimo':
                login_as(client, users[role])
            url = reverse(name, kwargs=kwargs) if kwargs else reverse(name)
            try:
                resp = getattr(client, method)(url)
                status = resp.status_code
                if status >= 500:
                    results.append((name, role, status, 'ERROR 500'))
                elif status == 403:
                    results.append((name, role, status, 'FORBIDDEN'))
                elif status == 401:
                    results.append((name, role, status, 'UNAUTHORIZED'))
                elif status == 302:
                    results.append((name, role, status, 'REDIRECT'))
                elif status == 200:
                    results.append((name, role, status, 'OK'))
                else:
                    results.append((name, role, status, 'OTHER'))
            except Exception as e:
                results.append((name, role, 'EXC', str(e)))
    print("\n--- RESULTADOS DE TEST DE VISTAS ---")
    for r in results:
        print(f"Vista: {r[0]:35} | Rol: {r[1]:12} | Status: {r[2]:6} | {r[3]}")
    print("\nResumen de vistas problemáticas:")
    for r in results:
        if r[2] in [500, 'EXC']:
            print(f"❌ {r}")
    print("\nTest finalizado.")

if __name__ == '__main__':
    test_routes() 