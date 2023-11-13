from app.models import Libro, Prestamo, PerfilUsuario
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DetailView

def index(request):
    return render(request, "index.html")

class DetalleLibro(DetailView):
    model = Libro
    template_name = 'detalle_libro.html'

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'lista_libros.html', {'libros': libros})

class RegistroUsuario(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def login(request):
    return render(request, "login.html")
