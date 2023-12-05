from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from .traductor import traducir
import os

from wsgiref.util import FileWrapper
import mimetypes

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

        # Guarda el archivo SRT temporalmente
        with open('temp.srt', 'wb+') as destination:
            for chunk in archivo_srt.chunks():
                destination.write(chunk)

        # Traduce el archivo SRT
        srt_traducido = traducir('temp.srt', idioma_destino)

        # Elimina el archivo temporal
        os.remove('temp.srt')

        response = HttpResponse(srt_traducido, content_type='application/srt')
        response['Content-Disposition'] = 'attachment; filename="traduccion.srt"'
        return response

    return render(request, 'core/traductor.html')


def lista_archivitos(request):
    query = request.GET.get('q')
    if query:
        archivitos = Archivito.objects.filter(Q(nombre__icontains=query) | Q(contenido__icontains=query))
    else:
        archivitos = Archivito.objects.all()
    return render(request, 'lista_archivitos.html', {'archivitos': archivitos, 'query': query})
    

def subir_archivito(request):
    if request.method == 'POST':
        form = ArchivitoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_archivitos')
    else:
        form = ArchivitoForm()

    return render(request, 'lista_archivitos.html', {'form': form})

def descargar_archivito(request, archivito_id):  
    archivito = get_object_or_404(Archivito, pk=archivito_id)
    
    response = HttpResponse(content_type=mimetypes.guess_type(archivito.nombre)[0])
    response['Content-Disposition'] = f'attachment; filename="{archivito.nombre}"'

    # Aquí se escribe el contenido del archivo en la respuesta
    response.write(archivito.contenido)

    return response

    #archivito = get_object_or_404(Archivito, pk=archivito_id)
    
    #response = HttpResponse(content_type=mimetypes.guess_type(archivito.nombre)[0])
    #response['Content-Disposition'] = f'attachment; filename="{archivito.nombre}"'

    #with open(archivito.contenido.path, 'rb') as file:
        #response.write(file.read())

    #return response



    #if request.method == 'POST':
        #form = ArchivitoForm(request.POST)
        #if form.is_valid():
            #form.save()        
            #return redirect('lista_archivitos')
    #else:
        #form = ArchivitoForm()       
    #return render(request, 'lista_archivitos.html', {'form': form})

    