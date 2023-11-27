from .models import Prestamo
from app.models import Libro, Prestamo
from django import forms
from django.forms import DateInput
from django.utils import timezone
from django.core.exceptions import ValidationError

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libros', 'fecha_prestamo', 'fecha_devolucion_estimada', 'solicitante']
        widgets = {
            'fecha_prestamo': DateInput(attrs={'type': 'date'}),
            'fecha_devolucion_estimada': DateInput(attrs={'type': 'date'}),
            'solicitante': forms.Select(attrs={'class': 'form-control', 'readonly': True}),
        }

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['numero_serie', 'titulo', 'anio_publicacion', 'autores', 'categorias', 'editorial', 'descripcion', 'stock', 'imagen']
        widgets = {
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'anio_publicacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'autores': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'editorial': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

