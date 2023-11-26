from .models import Prestamo
from app.models import Libro, Prestamo
from django import forms
from django.forms import DateInput

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libros', 'fecha_prestamo', 'fecha_devolucion_estimada', 'solicitante']
        widgets = {
            'fecha_prestamo': DateInput(attrs={'type': 'date'}),
            'fecha_devolucion_estimada': DateInput(attrs={'type': 'date'}),
        }

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['numero_serie', 'titulo', 'anio_publicacion', 'autores', 'categorias', 'editorial']