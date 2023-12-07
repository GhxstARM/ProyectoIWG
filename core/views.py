from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from .traductor import traducir
import os
import tempfile
from wsgiref.util import FileWrapper
import mimetypes
from django.core.files.base import ContentFile

from .models import Archivito, UserFile, HistorialTraducciones
from .forms import ArchivitoForm, UserFileForm
from django.utils import timezone



from django.db.models import Q


# Create your views here.
def home(request):
    return render(request, 'core/home.html')

@login_required
def archivos(request):
    return render(request, 'core/traducciones.html')

def salir(request):
    logout(request)
    return redirect('home')

def registrar(request):
    data = {
        'form': CustomUserCreationForm()

    }
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')

    return render(request, 'registration/register.html', data )

@login_required
def traductor(request):
    
    usuario = request.user
    hoy = timezone.now().date()
    traducciones_hoy = HistorialTraducciones.objects.filter(usuario=usuario, fecha=hoy).first()
    if traducciones_hoy and traducciones_hoy.cantidad_traducciones >= 3:  # Límite de 7 traducciones diarias
        # El usuario ha alcanzado el límite, redirigir o mostrar un mensaje de error
        return render(request, 'no_more.html')



    if request.method == 'POST':
        srt_file = request.FILES['srt_file']
        target_language = request.POST.get('target_language')
        
        

        if not target_language or not srt_file:
            return HttpResponse("Debes proporcionar un idioma de destino y un archivo SRT.")

        with open('temp.srt', 'wb+') as destination:
            for chunk in srt_file.chunks():
                destination.write(chunk)


        
        srt_traducido = traducir('temp.srt', target_language)

    
        os.remove('temp.srt')

        if traducciones_hoy:
            traducciones_hoy.cantidad_traducciones += 1
            traducciones_hoy.archivo.save('traduccion.srt', ContentFile(srt_traducido))
            traducciones_hoy.save()
        else:
            HistorialTraducciones.objects.create(usuario=usuario, cantidad_traducciones=1, archivo=ContentFile(srt_traducido, 'traduccion.srt'))

            

        response = HttpResponse(srt_traducido, content_type='application/srt')
        response['Content-Disposition'] = 'attachment; filename="traduccion.srt"'
        return response

    return render(request, 'core/translate.html')

@login_required
def lista_archivitos(request):
    query_nombre = request.GET.get('q_nombre', '')
    query_contenido = request.GET.get('q_contenido', '')

    if query_nombre or query_contenido:
        results = Archivito.objects.filter(Q(nombre__icontains=query_nombre) & Q(contenido__icontains=query_contenido))
    else:
        results = []

    context = {'archivitos': results, 'query_nombre': query_nombre, 'query_contenido': query_contenido}
    return render(request, 'lista_archivitos.html', context)


@login_required
def descargar_archivito(request, archivito_id):
    archivito = get_object_or_404(Archivito, id=archivito_id)

    response = HttpResponse(archivito.contenido, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename={archivito.nombre}'

    return response

@login_required
def subir_archivito(request):
    if request.method == 'POST':
        form = ArchivitoForm(request.POST, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            contenido = form.cleaned_data['contenido'].read().decode('utf-8')
            Archivito.objects.create(nombre=nombre, contenido=contenido)
            return redirect('lista_archivitos')
    else:
        form = ArchivitoForm()
    return render(request, 'subir_archivito.html', {'form': form})



# Vistas relacionadas con La lista personal de cada usuario

@login_required
def archivos_usuario(request):
    # Obtén los archivos asociados al usuario actual
    archivos = HistorialTraducciones.objects.filter(usuario=request.user)

    context = {'archivos': archivos}
    return render(request, 'core/traducciones.html', context)

@login_required
def guardar_archivo(request):
    if request.method == 'POST':
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_archivo = form.save(commit=False)
            nuevo_archivo.user = request.user
            nuevo_archivo.save()
            return redirect('archivos_usuario')
    else:
        form = UserFileForm()
    return render(request, 'core/traducciones.html', {'form': form})


@login_required
def eliminar_archivo(request, archivo_id):
    archivo = get_object_or_404(UserFile, id=archivo_id, user=request.user)
    archivo.delete()
    return redirect('archivos_usuario')