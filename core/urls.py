"""
URL configuration for ProyectoIWG project.

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

from django.urls import path
from .views import home, archivos, salir, registrar, traductor, lista_archivitos, subir_archivito, descargar_archivito, guardar_archivo, archivos_usuario, eliminar_archivo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('archivos/', archivos, name='archivos'),
    path('logout/', salir, name='salir'),
    path('register/', registrar, name='registrar'),
    path('translate/', traductor, name='traductor'),
    path('archivitos/', lista_archivitos, name='lista_archivitos'),
    path('subir_archivito/', subir_archivito, name='subir_archivito'),
    path('descargar_archivito/<int:archivito_id>/', descargar_archivito, name='descargar_archivito'),
    path('guardar_archivo/', guardar_archivo, name='guardar_archivo'),
    path('archivos_usuario/', archivos_usuario, name='archivos_usuario'),
    path('eliminar_archivo/<int:archivo_id>/', eliminar_archivo, name='eliminar_archivo'),

    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)