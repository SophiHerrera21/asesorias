from django.utils.deprecation import MiddlewareMixin
from .models import RegistroAuditoria

class AuditoriaMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Guardar el usuario y la IP para uso posterior
        request._audit_user = getattr(request, 'user', None)
        request._audit_ip = self.get_client_ip(request)
        request._audit_user_agent = request.META.get('HTTP_USER_AGENT', '')

    def process_response(self, request, response):
        # Registrar inicio de sesión
        if hasattr(request, 'user') and request.user.is_authenticated:
            if not hasattr(request, '_audit_user') or request._audit_user != request.user:
                RegistroAuditoria.registrar(
                    usuario=request.user,
                    tipo_accion='login',
                    descripcion=f'Inicio de sesión desde {request._audit_ip}',
                    ip_address=request._audit_ip,
                    user_agent=request._audit_user_agent
                )

        # Registrar cierre de sesión
        if hasattr(request, '_audit_user') and request._audit_user and not request.user.is_authenticated:
            RegistroAuditoria.registrar(
                usuario=request._audit_user,
                tipo_accion='logout',
                descripcion=f'Cierre de sesión desde {request._audit_ip}',
                ip_address=request._audit_ip,
                user_agent=request._audit_user_agent
            )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip 