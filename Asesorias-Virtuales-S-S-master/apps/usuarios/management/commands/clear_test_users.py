from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Elimina todos los usuarios de prueba de forma segura.'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            self.stdout.write(self.style.WARNING('Eliminando usuarios de prueba...'))
            
            # Eliminar en orden para evitar problemas de foreign key
            cursor.execute("DELETE FROM apps_usuarios_coordinador")
            self.stdout.write("✅ Coordinadores eliminados")
            
            cursor.execute("DELETE FROM apps_usuarios_asesor")
            self.stdout.write("✅ Asesores eliminados")
            
            cursor.execute("DELETE FROM apps_usuarios_aprendiz")
            self.stdout.write("✅ Aprendices eliminados")
            
            cursor.execute("DELETE FROM apps_usuarios_usuario")
            self.stdout.write("✅ Usuarios eliminados")
            
        self.stdout.write(self.style.SUCCESS('¡Base de datos limpia!')) 