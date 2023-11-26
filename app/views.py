from .forms import LibroForm, PrestamoForm
from app.models import Libro, Prestamo, HistorialMovimientos
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator
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

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                datos = { 'usuario': user, 'mensaje': f'Bienvenido {user.username}!', 'info': 'login'}
                historial = f'{user.username} inició sesión'
                registrar_uso(user, historial)
                return render(request, 'index.html', datos)
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    return render(request, 'confirm_logout.html')

@login_required
def user_logout(request):
    accion = f"{request.user.username} cerró sesión"
    registrar_uso(request.user, accion)
    logout(request)
    datos = { 'info': 'logout', 'mensaje': 'Has cerrado sesión exitosamente.'}
    return render(request, 'index.html', datos)

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

@login_required
def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            accion = f"{request.user.username} creó el libro {form.cleaned_data['titulo']}"
            registrar_uso(request.user, accion, 'libro')
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
            accion = f"{request.user.username} actualizó el libro {form.cleaned_data['titulo']}"
            registrar_uso(request.user, accion)
            return redirect('detalle_libro', pk=pk)
    else:
        form = LibroForm(instance=libro)
    return render(request, 'libro_form.html', {'form': form})

@login_required
def eliminar_libro(request, pk):
    if request.method == 'POST':
        accion = f"{request.user.username} eliminó el libro {Libro.objects.get(pk=pk).titulo}"
        registrar_uso(request.user, accion)
        Libro.objects.filter(pk=pk).delete()
    return redirect('lista_libros')


@login_required
def manejar_prestamo(request, pk=None):
    prestamo = None
    if pk:
        prestamo = get_object_or_404(Prestamo, pk=pk)
        form = PrestamoForm(request.POST or None, instance=prestamo)
    else:
        form = PrestamoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        accion = f"{request.user.username} pidió prestado '{form.cleaned_data['libros'][0]}'"
        registrar_uso(request.user, accion, 'prestamo')
        return redirect('lista-libros')

    return render(request, 'prestamo.html', {'form': form, 'prestamo': prestamo})

@login_required
def eliminar_prestamo(request, pk):
    Prestamo.objects.filter(pk=pk).delete()
    accion = f"{request.user.username} eliminó el prestamo {Prestamo.objects.get(pk=pk)}"
    registrar_uso(request.user, accion, 'prestamo')
    return redirect('lista_prestamos')

@login_required
def marcar_devuelto(request, pk):
    prestamo = Prestamo.objects.get(pk=pk)
    prestamo.estado = 'Devuelto'
    prestamo.save()
    accion = f"{request.user.username} marcó como devuelto el prestamo {Prestamo.objects.get(pk=pk)}"
    registrar_uso(request.user, accion, 'prestamo')
    return redirect('prestamos')

@login_required
def lista_prestamos(request):
    prestamos = Prestamo.objects.all().filter(solicitante=request.user).order_by('-fecha_prestamo')
    if not prestamos:
        return render(request, 'mis_prestamos.html', {'mensaje': 'No tienes préstamos'})
    
    # Configuración de la paginación
    paginator = Paginator(prestamos, 10)
    page = request.GET.get('page')
    prestamos = paginator.get_page(page)

    return render(request, 'mis_prestamos.html', {'prestamos': prestamos})

@login_required
def lista_todos_prestamos(request):
    prestamos = Prestamo.objects.all().order_by('-fecha_prestamo')

    # Configuración de la paginación
    paginator = Paginator(prestamos, 10)
    page = request.GET.get('page')
    prestamos = paginator.get_page(page)

    return render(request, 'lista_prestamos.html', {'prestamos': prestamos})

@login_required
def lista_historial(request):
    # Obtiene todos los historiales y los ordena por fecha
    historiales_list = HistorialMovimientos.objects.all().order_by('-fecha')

    # Configuración de la paginación
    paginator = Paginator(historiales_list, 10) # Muestra 10 historiales por página
    page = request.GET.get('page')
    historiales = paginator.get_page(page)

    return render(request, 'historial.html', {'historiales': historiales})

class DetallePrestamo(DetailView):
    model = Prestamo
    template_name = 'detalle_prestamo.html'

def registrar_uso(user, accion, tabla=None):
    # guardar en HistorialMovimientos
    datos = { 'usuario': user, 'accion': accion, 'tabla': tabla }
    HistorialMovimientos.objects.create(**datos)



    