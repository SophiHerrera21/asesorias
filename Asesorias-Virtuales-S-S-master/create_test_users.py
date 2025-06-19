import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asesorias_virtuales.settings')
django.setup()

from apps.usuarios.models import Usuario

def create_test_users():
    # Crear usuario aprendiz
    aprendiz = Usuario.objects.create_user(
        username='aprendiz@test.com',
        email='aprendiz@test.com',
        password='Aprendiz123!',
        first_name='Juan',
        last_name='Pérez',
        role='aprendiz',
        telefono='3001234567',
        direccion='Calle 123 #45-67'
    )
    print(f"Usuario aprendiz creado: {aprendiz}")

    # Crear usuario asesor
    asesor = Usuario.objects.create_user(
        username='asesor@test.com',
        email='asesor@test.com',
        password='Asesor123!',
        first_name='María',
        last_name='González',
        role='asesor',
        telefono='3007654321',
        direccion='Carrera 78 #90-12'
    )
    print(f"Usuario asesor creado: {asesor}")

    # Crear usuario coordinador
    coordinador = Usuario.objects.create_user(
        username='coordinador@test.com',
        email='coordinador@test.com',
        password='Coordinador123!',
        first_name='Carlos',
        last_name='Rodríguez',
        role='coordinador',
        telefono='3009876543',
        direccion='Avenida 5 #23-45'
    )
    print(f"Usuario coordinador creado: {coordinador}")

if __name__ == '__main__':
    create_test_users() 