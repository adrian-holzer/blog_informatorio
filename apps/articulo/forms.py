# articulo/forms.py

from django import forms
from .models import Articulo

from django.forms.widgets import ClearableFileInput




class ArticuloForm(forms.ModelForm):

  
    class Meta:
        model = Articulo

        
        # Excluimos 'editor', 'fecha_publicacion' y 'publicado' 
        # porque los asignaremos automáticamente en la vista.
        fields = ('titulo', 'resumen', 'contenido', 'categoria', 'imagen')
        
        # Opcional: añade clases para darle un estilo (asumiendo Bootstrap)
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': ClearableFileInput(attrs={'allow_clear': False}),
        }