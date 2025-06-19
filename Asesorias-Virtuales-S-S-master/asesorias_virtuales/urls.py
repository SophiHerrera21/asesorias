"""
URL configuration for asesorias_virtuales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.usuarios.views import exportar_pdf_usuarios_componentes_grupos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls')),
    path('notificaciones/', include('apps.notificaciones.urls')),
    path('grupos/', include('apps.grupos.urls')),
    path('reportes/', include('apps.reportes.urls')),
    path('pqrs/', include('apps.pqrs.urls')),
    path('asesorias/', include('apps.asesorias.urls')),
    path('pruebas/', include('apps.pruebas.urls')),
    path('exportar-pdf/', exportar_pdf_usuarios_componentes_grupos, name='exportar_pdf_usuarios_componentes_grupos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
