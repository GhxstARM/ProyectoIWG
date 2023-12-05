from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Archivito

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class ArchivitoForm(forms.ModelForm):
    class Meta:
        model = Archivito
        fields = ['nombre', 'contenido']
    contenido = forms.FileField()