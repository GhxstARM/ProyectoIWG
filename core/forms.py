from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Archivito

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


