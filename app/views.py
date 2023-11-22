from app.models import Libro, Prestamo, PerfilUsuario
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404
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
    return render(request, 'login.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirigir a una página de inicio exitoso, por ejemplo, el dashboard del usuario
                return redirect('dashboard')
            else:
                # Manejar usuarios que están deshabilitados o inactivos
                return render(request, 'login.html', {'error': 'Tu cuenta está desactivada.'})
        else:
            # Manejar credenciales incorrectas
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        # Mostrar la página de inicio de sesión si no es una solicitud POST
        return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'username': request.user.username})

def user_logout(request):
    if request.method == "POST":
        logout(request)
        # Redirigir a la página de inicio o de cierre de sesión exitoso
        return redirect('index')
    else:
        # Mostrar una página o un diálogo de confirmación antes de cerrar sesión
        return render(request, 'confirm_logout.html', {'username': request.user.username})

@login_required
def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = LibroForm()
    return render(request, 'libro_form.html', {'form': form})

@login_required
def actualizar_libro(request, pk):
    libro = Libro.objects.get(pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('detalle_libro', pk=pk)
    else:
        form = LibroForm(instance=libro)
    return render(request, 'libro_form.html', {'form': form})

@login_required
def eliminar_libro(request, pk):
    Libro.objects.filter(pk=pk).delete()
    return redirect('lista_libros')

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['numero_serie', 'titulo', 'anio_publicacion', 'autores', 'categorias', 'editorial']

@login_required
def crear_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_prestamos')
    else:
        form = PrestamoForm()
    return render(request, 'prestamo_form.html', {'form': form})

@login_required
def actualizar_prestamo(request, pk):
    prestamo = Prestamo.objects.get(pk=pk)
    if request.method == 'POST':
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect('detalle_prestamo', pk=pk)
    else:
        form = PrestamoForm(instance=prestamo)
    return render(request, 'prestamo_form.html', {'form': form})

@login_required
def eliminar_prestamo(request, pk):
    Prestamo.objects.filter(pk=pk).delete()
    return redirect('lista_prestamos')

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libros', 'fecha_prestamo', 'fecha_devolucion_estimada', 'fecha_devolucion_real', 'dias_retraso', 'multa', 'costo_prestamo', 'solicitante']

@login_required
def lista_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'lista_prestamos.html', {'prestamos': prestamos})

class DetallePrestamo(DetailView):
    model = Prestamo
    template_name = 'detalle_prestamo.html'