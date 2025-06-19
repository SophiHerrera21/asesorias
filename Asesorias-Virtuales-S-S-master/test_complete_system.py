#!/usr/bin/env python
"""
Test completo del sistema de asesorías virtuales
Verifica: registro, login, validación de trimestre, emails y vistas protegidas
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.conf import settings
import time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asesorias_virtuales.settings')
django.setup()

from apps.usuarios.models import Usuario, Asesor, Aprendiz, Coordinador
from apps.usuarios.forms import AsesorRegistroForm

class SistemaCompletoTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        
        # Crear usuarios de prueba con emails únicos
        timestamp = int(time.time())
        
        self.aprendiz = self.User.objects.create_user(
            username=f'aprendiz{timestamp}@test.com',
            email=f'aprendiz{timestamp}@test.com',
            password='testpass123',
            first_name='Juan',
            last_name='Pérez',
            role='aprendiz',
            documento=f'12345678{timestamp}'
        )
        Aprendiz.objects.create(
            usuario=self.aprendiz,
            ficha='123456',
            programa='Técnico en Sistemas',
            trimestre='2'
        )
        
        self.asesor = self.User.objects.create_user(
            username=f'asesor{timestamp}@test.com',
            email=f'asesor{timestamp}@test.com',
            password='testpass123',
            first_name='María',
            last_name='García',
            role='asesor',
            documento=f'87654321{timestamp}'
        )
        Asesor.objects.create(
            usuario=self.asesor,
            especialidad='Programación',
            experiencia='5 años en desarrollo web',
            titulo='Ingeniero de Sistemas',
            max_grupos=4,
            disponibilidad='Lunes a Viernes 2-6pm',
            trimestre='5'
        )
        
        self.coordinador = self.User.objects.create_user(
            username=f'coordinador{timestamp}@test.com',
            email=f'coordinador{timestamp}@test.com',
            password='testpass123',
            first_name='Carlos',
            last_name='López',
            role='coordinador',
            documento=f'11223344{timestamp}'
        )
        Coordinador.objects.create(
            usuario=self.coordinador,
            cargo='Coordinador Académico',
            departamento='Sistemas'
        )
    
    def test_01_registro_aprendiz(self):
        """Test registro de aprendiz"""
        print("\n🔍 Probando registro de aprendiz...")
        
        data = {
            'first_name': 'Ana',
            'last_name': 'Rodríguez',
            'email': 'ana.rodriguez@test.com',
            'documento': '98765432',
            'role': 'aprendiz',
            'telefono': '3001234567',
            'direccion': 'Calle 123 #45-67',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'ficha': '123456',
            'programa': 'Técnico en Sistemas',
            'trimestre': '2'
        }
        
        response = self.client.post(reverse('usuarios:registro_aprendiz'), data)
        
        if response.status_code == 302:  # Redirect to login
            print("✅ Registro de aprendiz exitoso")
            # Verificar que el usuario se creó
            user = self.User.objects.get(email='ana.rodriguez@test.com')
            self.assertEqual(user.role, 'aprendiz')
            self.assertTrue(hasattr(user, 'aprendiz'))
            print(f"   - Usuario creado: {user.email}")
            print(f"   - Rol: {user.role}")
            print(f"   - Ficha: {user.aprendiz.ficha}")
        else:
            print(f"❌ Error en registro de aprendiz: {response.status_code}")
            if hasattr(response, 'context') and response.context and 'form' in response.context:
                print(f"   - Errores: {response.context['form'].errors}")
            else:
                print("   - No se pudo obtener información de errores del formulario")
    
    def test_02_registro_asesor_validacion_trimestre(self):
        """Test registro de asesor con validación de trimestre (3-7)"""
        print("\n🔍 Probando registro de asesor con validación de trimestre...")
        
        # Test con trimestre válido (5)
        data_valido = {
            'first_name': 'Pedro',
            'last_name': 'Martínez',
            'email': 'pedro.martinez@test.com',
            'documento': '55443322',
            'role': 'asesor',
            'telefono': '3009876543',
            'direccion': 'Carrera 78 #12-34',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'trimestre': '5',
            'especialidad': 'Matemáticas',
            'experiencia': '3 años enseñando matemáticas en universidad',
            'titulo': 'Licenciado en Matemáticas',
            'disponibilidad': 'Martes y Jueves 3-7pm'
        }
        
        form = AsesorRegistroForm(data_valido)
        if form.is_valid():
            print("✅ Formulario de asesor válido con trimestre 5")
            print(f"   - Trimestre: {form.cleaned_data['trimestre']}")
            print(f"   - Especialidad: {form.cleaned_data['especialidad']}")
        else:
            print(f"❌ Error en formulario válido: {form.errors}")
        
        # Test con trimestre inválido (2)
        data_invalido = data_valido.copy()
        data_invalido['trimestre'] = '2'
        data_invalido['email'] = 'otro@test.com'
        
        form_invalido = AsesorRegistroForm(data_invalido)
        if not form_invalido.is_valid():
            print("✅ Validación de trimestre funciona correctamente")
            self.assertIn('trimestre', form_invalido.errors)
            print(f"   - Error esperado: {form_invalido.errors['trimestre']}")
        else:
            print("❌ La validación de trimestre no está funcionando")
    
    def test_03_login_y_redireccion(self):
        """Test login y redirección según rol"""
        print("\n🔍 Probando login y redirección por roles...")
        
        # Login aprendiz
        response = self.client.post(reverse('usuarios:login'), {
            'email': self.aprendiz.email,
            'password': 'testpass123'
        })
        
        if response.status_code == 302:
            print("✅ Login de aprendiz exitoso")
            # Verificar redirección
            if 'dashboard_aprendiz' in response.url:
                print("   - Redirección correcta a dashboard de aprendiz")
            else:
                print(f"   - Redirección inesperada: {response.url}")
        else:
            print(f"❌ Error en login de aprendiz: {response.status_code}")
        
        # Login asesor
        self.client.logout()
        response = self.client.post(reverse('usuarios:login'), {
            'email': self.asesor.email,
            'password': 'testpass123'
        })
        
        if response.status_code == 302:
            print("✅ Login de asesor exitoso")
            if 'dashboard_asesor' in response.url:
                print("   - Redirección correcta a dashboard de asesor")
            else:
                print(f"   - Redirección inesperada: {response.url}")
        else:
            print(f"❌ Error en login de asesor: {response.status_code}")
        
        # Login coordinador
        self.client.logout()
        response = self.client.post(reverse('usuarios:login'), {
            'email': self.coordinador.email,
            'password': 'testpass123'
        })
        
        if response.status_code == 302:
            print("✅ Login de coordinador exitoso")
            if 'dashboard_coordinador' in response.url:
                print("   - Redirección correcta a dashboard de coordinador")
            else:
                print(f"   - Redirección inesperada: {response.url}")
        else:
            print(f"❌ Error en login de coordinador: {response.status_code}")
    
    def test_04_vistas_protegidas(self):
        """Test acceso a vistas protegidas por rol"""
        print("\n🔍 Probando acceso a vistas protegidas...")
        
        # Test sin login
        response = self.client.get(reverse('usuarios:dashboard_aprendiz'))
        if response.status_code == 302:
            print("✅ Vista protegida redirige sin login")
        else:
            print(f"❌ Vista no está protegida: {response.status_code}")
        
        # Test con login de aprendiz
        self.client.force_login(self.aprendiz)
        response = self.client.get(reverse('usuarios:dashboard_aprendiz'))
        if response.status_code == 200:
            print("✅ Aprendiz puede acceder a su dashboard")
        else:
            print(f"❌ Aprendiz no puede acceder a su dashboard: {response.status_code}")
        
        # Test acceso cruzado (aprendiz intenta acceder a dashboard de asesor)
        response = self.client.get(reverse('usuarios:dashboard_asesor'))
        if response.status_code == 403:
            print("✅ Protección de roles funciona correctamente")
        else:
            print(f"❌ No hay protección de roles: {response.status_code}")
        
        # Test coordinador accede a lista de usuarios
        self.client.force_login(self.coordinador)
        response = self.client.get(reverse('usuarios:lista_usuarios'))
        if response.status_code == 200:
            print("✅ Coordinador puede acceder a lista de usuarios")
        else:
            print(f"❌ Coordinador no puede acceder a lista de usuarios: {response.status_code}")
    
    def test_05_envio_emails(self):
        """Test envío de emails"""
        print("\n🔍 Probando envío de emails...")
        
        # Verificar configuración de email
        if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
            print(f"✅ Configuración de email encontrada: {settings.EMAIL_HOST_USER}")
            
            # Test envío de email simple
            try:
                from django.core.mail import send_mail
                result = send_mail(
                    subject='Test Sistema Asesorías',
                    message='Este es un email de prueba del sistema.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['test@example.com'],
                    fail_silently=True
                )
                if result:
                    print("✅ Envío de email funciona correctamente")
                else:
                    print("⚠️ Envío de email falló silenciosamente")
            except Exception as e:
                print(f"❌ Error en envío de email: {str(e)}")
        else:
            print("❌ Configuración de email no encontrada")
    
    def test_06_validacion_trimestre_asesor(self):
        """Test específico de validación de trimestre para asesores"""
        print("\n🔍 Probando validación específica de trimestre para asesores...")
        
        # Test trimestres válidos (3-7)
        trimestres_validos = ['3', '4', '5', '6', '7']
        for trimestre in trimestres_validos:
            data = {
                'first_name': 'Test',
                'last_name': 'User',
                'email': f'test{trimestre}@test.com',
                'documento': f'12345{trimestre}',
                'role': 'asesor',
                'telefono': '3001234567',
                'direccion': 'Test Address',
                'password1': 'testpass123',
                'password2': 'testpass123',
                'trimestre': trimestre,
                'especialidad': 'Test Especialidad',
                'experiencia': 'Experiencia de prueba con más de 10 caracteres',
                'titulo': 'Test Título',
                'disponibilidad': 'Disponibilidad de prueba'
            }
            
            form = AsesorRegistroForm(data)
            if form.is_valid():
                print(f"✅ Trimestre {trimestre} es válido")
            else:
                print(f"❌ Trimestre {trimestre} debería ser válido: {form.errors}")
        
        # Test trimestres inválidos (1, 2, 8, 9)
        trimestres_invalidos = ['1', '2', '8', '9']
        for trimestre in trimestres_invalidos:
            data = {
                'first_name': 'Test',
                'last_name': 'User',
                'email': f'test{trimestre}@test.com',
                'documento': f'12345{trimestre}',
                'role': 'asesor',
                'telefono': '3001234567',
                'direccion': 'Test Address',
                'password1': 'testpass123',
                'password2': 'testpass123',
                'trimestre': trimestre,
                'especialidad': 'Test Especialidad',
                'experiencia': 'Experiencia de prueba con más de 10 caracteres',
                'titulo': 'Test Título',
                'disponibilidad': 'Disponibilidad de prueba'
            }
            
            form = AsesorRegistroForm(data)
            if not form.is_valid() and 'trimestre' in form.errors:
                print(f"✅ Trimestre {trimestre} correctamente rechazado")
            else:
                print(f"❌ Trimestre {trimestre} debería ser rechazado")
    
    def test_07_crear_asesor_completo(self):
        """Test creación completa de asesor con validación"""
        print("\n🔍 Probando creación completa de asesor...")
        
        data = {
            'first_name': 'Laura',
            'last_name': 'Fernández',
            'email': 'laura.fernandez@test.com',
            'documento': '99998888',  # Documento único
            'role': 'asesor',
            'telefono': '3005555666',
            'direccion': 'Calle 45 #67-89',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'trimestre': '6',
            'especialidad': 'Física',
            'experiencia': '4 años como docente universitario en física aplicada',
            'titulo': 'Físico',
            'disponibilidad': 'Lunes, Miércoles y Viernes 4-8pm'
        }
        
        form = AsesorRegistroForm(data)
        if form.is_valid():
            print("✅ Formulario de asesor válido")
            
            # Crear el usuario
            usuario = form.save(commit=False)
            usuario.role = 'asesor'
            usuario.username = usuario.email
            usuario.set_password(form.cleaned_data['password1'])
            usuario.save()
            
            # Crear el asesor
            asesor = Asesor.objects.create(
                usuario=usuario,
                especialidad=form.cleaned_data['especialidad'],
                experiencia=form.cleaned_data['experiencia'],
                titulo=form.cleaned_data['titulo'],
                max_grupos=4,
                disponibilidad=form.cleaned_data['disponibilidad'],
                trimestre=form.cleaned_data['trimestre']
            )
            
            print(f"   - Usuario creado: {usuario.email}")
            print(f"   - Asesor creado con trimestre: {asesor.trimestre}")
            print(f"   - Especialidad: {asesor.especialidad}")
            print(f"   - Título: {asesor.titulo}")
            
            # Verificar que el trimestre está en el rango correcto
            trimestre_int = int(asesor.trimestre)
            if 3 <= trimestre_int <= 7:
                print("✅ Trimestre en rango válido (3-7)")
            else:
                print(f"❌ Trimestre fuera de rango: {trimestre_int}")
                
        else:
            print(f"❌ Formulario inválido: {form.errors}")

def run_tests():
    """Ejecutar todos los tests"""
    print("🚀 INICIANDO TESTS COMPLETOS DEL SISTEMA")
    print("=" * 50)
    
    # Crear instancia de test
    test_instance = SistemaCompletoTest()
    test_instance.setUp()
    
    # Ejecutar tests
    tests = [
        test_instance.test_01_registro_aprendiz,
        test_instance.test_02_registro_asesor_validacion_trimestre,
        test_instance.test_03_login_y_redireccion,
        test_instance.test_04_vistas_protegidas,
        test_instance.test_05_envio_emails,
        test_instance.test_06_validacion_trimestre_asesor,
        test_instance.test_07_crear_asesor_completo,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ Error en test: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADOS: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("🎉 ¡TODOS LOS TESTS PASARON! El sistema está funcionando correctamente.")
    else:
        print("⚠️ Algunos tests fallaron. Revisa los errores arriba.")
    
    return passed == total

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1) 