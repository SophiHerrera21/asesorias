from functools import wraps
from .models import RegistroAuditoria

def auditar(tipo_accion, descripcion=None):
    """
    Decorador para registrar acciones en la auditoría
    
    Uso:
    @auditar('create', 'Creación de prueba')
    def crear_prueba(request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Ejecutar la vista
            response = view_func(request, *args, **kwargs)
            
            # Registrar la acción
            if request.user.is_authenticated:
                desc = descripcion
                if callable(descripcion):
                    desc = descripcion(request, *args, **kwargs)
                
                RegistroAuditoria.registrar(
                    usuario=request.user,
                    tipo_accion=tipo_accion,
                    descripcion=desc,
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
            
            return response
        return wrapped_view
    return decorator 