from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Archivito, UserFile, HistorialTraducciones

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class ArchivitoForm(forms.ModelForm):
    contenido = forms.FileField(widget=forms.FileInput)  # Modificado a FileInput

    class Meta:
        model = Archivito
        fields = ['nombre', 'contenido']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True


class UserFileForm(forms.ModelForm):
    class Meta:
        model = HistorialTraducciones
        fields = ['archivo']


class SRTFileForm(forms.Form):
    language_choices = [
        ('de', 'Aleman'),
        ('es', 'Español'),
        ('fr', 'Frances'),
        ('en', 'Ingles'),
        ('nl', 'Holandés'),
        ('it', 'Italiano'),
        ('pt', 'Portugués'),
        ('ht','Criollo haitiano'),
        ('da', 'Danés'),
        
        
    ]

    
    target_language = forms.ChoiceField(choices=language_choices, label='Idioma de destino', widget=forms.Select(attrs={'class': 'form-control'}))
