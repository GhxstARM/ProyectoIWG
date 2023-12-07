from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from .traductor import traducir
import os

from wsgiref.util import FileWrapper
import mimetypes
from django.core.files.base import ContentFile

from .models import Archivito
from .forms import ArchivitoForm
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

def traductor(request):
    if request.method == 'POST':
        idioma_destino = request.POST.get('idioma_destino')
        archivo_srt = request.FILES.get('archivo_srt')

        if not idioma_destino or not archivo_srt:
            return HttpResponse("Debes proporcionar un idioma de destino y un archivo SRT.")

        with open('temp.srt', 'wb+') as destination:
            for chunk in archivo_srt.chunks():
                destination.write(chunk)

        
        srt_traducido = traducir('temp.srt', idioma_destino)

    
        os.remove('temp.srt')

        response = HttpResponse(srt_traducido, content_type='application/srt')
        response['Content-Disposition'] = 'attachment; filename="traduccion.srt"'
        return response

    return render(request, 'core/traductor.html')

def lista_archivitos(request):
    query_nombre = request.GET.get('q_nombre', '')
    query_contenido = request.GET.get('q_contenido', '')

    if query_nombre or query_contenido:
        results = Archivito.objects.filter(Q(nombre__icontains=query_nombre) & Q(contenido__icontains=query_contenido))
    else:
        results = []

    context = {'archivitos': results, 'query_nombre': query_nombre, 'query_contenido': query_contenido}
    return render(request, 'lista_archivitos.html', context)

#def lista_archivitos(request):
    query_nombre = request.GET.get('q_nombre', '')
    query_contenido = request.GET.get('q_contenido', '')

    if query_nombre:
        results = Archivito.objects.filter(nombre__icontains=query_nombre)
        if query_contenido:
            results = results.filter(contenido__icontains=query_contenido)
    elif query_contenido:
        results = Archivito.objects.filter(contenido__icontains=query_contenido)
    else:
        results = Archivito.objects.all()

    context = {'archivitos': results, 'query_nombre': query_nombre, 'query_contenido': query_contenido}
    return render(request, 'lista_archivitos.html', context)


def descargar_archivito(request, archivito_id):
    archivito = get_object_or_404(Archivito, id=archivito_id)

    response = HttpResponse(archivito.contenido, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename={archivito.nombre}'

    return response
#def lista_archivitos(request):
    query_nombre = request.GET.get('q_nombre', '')
    query_contenido = request.GET.get('q_contenido', '')

    if query_nombre or query_contenido:
        results = Archivito.objects.filter(
            Q(nombre__icontains=query_nombre) & Q(contenido__icontains=query_contenido)
        )
    else:
        results = Archivito.objects.all()

    context = {'archivitos': results, 'query_nombre': query_nombre, 'query_contenido': query_contenido}
    return render(request, 'lista_archivitos.html', context)


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

#def descargar_archivito(request, archivito_id):
    archivito = get_object_or_404(Archivito, id=archivito_id)

    response = HttpResponse(archivito.contenido, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename={archivito.nombre}'

    return response
#def descargar_archivito(request, archivito_id):  
    archivito = get_object_or_404(Archivito, pk=archivito_id)
    
    response = HttpResponse(content_type=mimetypes.guess_type(archivito.nombre)[0])
    response['Content-Disposition'] = f'attachment; filename="{archivito.nombre}"'

    response.write(archivito.contenido)

    return response

    