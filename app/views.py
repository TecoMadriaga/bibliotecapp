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
from django.contrib.auth.models import User, Group

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
                historial = f'Inició sesión'
                registrar_uso(user, historial, 'User')
                return render(request, 'index.html', datos)
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


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
def user_logout(request):
    accion = f"Cerró sesión"
    registrar_uso(request.user, accion, 'User')
    logout(request)
    datos = { 'info': 'logout', 'mensaje': 'Has cerrado sesión exitosamente.'}
    return render(request, 'index.html', datos)

@login_required
def crear_libro(request):
    if request.user.groups.filter(name='bibliotecario').exists():
        if request.method == 'POST':
            form = LibroForm(request.POST)
            if form.is_valid():
                form.save()
                accion = f"Creó el libro {form.cleaned_data['titulo']}"
                registrar_uso(request.user, accion, 'Libro')
                datos = { 'info': 'libro', 'mensaje': f'Has creado el libro {form.cleaned_data["titulo"]} exitosamente.', 'libros': Libro.objects.all()}
                return render(request, 'lista_libros.html', datos)
        else:
            form = LibroForm()
        return render(request, 'libro_form.html', {'form': form})
    else:
        group_error = f"No tienes permisos para acceder a esta página."
        return render(request, 'index.html', {'group_error': group_error})

@login_required
def editar_libro(request, pk):
    if request.user.groups.filter(name='bibliotecario').exists():
        libro = Libro.objects.get(pk=pk)
        if request.method == 'POST':
            form = LibroForm(request.POST, instance=libro)
            if form.is_valid():
                form.save()
                accion = f"Actualizó el libro '{form.cleaned_data['titulo']}'"
                registrar_uso(request.user, accion, 'Libro')
                datos = { 'info': 'libro', 'mensaje': f'Has actualizado el libro {form.cleaned_data["titulo"]} exitosamente.', 'libros': Libro.objects.all()}
                return render(request, 'lista_libros.html', datos)
        else:
            form = LibroForm(instance=libro)
        return render(request, 'libro_form.html', {'form': form})
    else:
        group_error = f"No tienes permisos para acceder a esta página."
        return render(request, 'index.html', {'group_error': group_error})

@login_required
def eliminar_libro(request, pk):
    if request.user.groups.filter(name='bibliotecario').exists():
        if request.method == 'POST':
            accion = f"Eliminó el libro '{Libro.objects.get(pk=pk).titulo}'"
            registrar_uso(request.user, accion, 'Libro')
            Libro.objects.filter(pk=pk).delete()
            datos = { 'info': 'libro', 'mensaje': f'Has eliminado el libro exitosamente.', 'libros': Libro.objects.all()}
            return render(request, 'lista_libros.html', datos)
        return redirect('lista_libros')
    else:
        group_error = f"No tienes permisos para acceder a esta página."
        return render(request, 'index.html', {'group_error': group_error})

@login_required
def manejar_prestamo(request, pk):
    if 'nuevo' in request.path:
        return manejar_nuevo_prestamo(request, pk)
    else:
        return manejar_actualizar_prestamo(request, pk)

def manejar_nuevo_prestamo(request, libro_pk):
    libro = get_object_or_404(Libro, pk=libro_pk)
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            # actualizar stock del libro
            if libro.stock > 0:
                libro.stock -= 1
            else:
                datos = { 'info': 'prestamo', 'mensaje': f'No hay stock disponible para el libro {libro.titulo}.', 'libros': Libro.objects.all()}
                return render(request, 'lista_libros.html', datos)
            libro.save()
            registrar_uso(request.user, f"Pidió prestado '{libro.titulo}'", 'Prestamo')
            datos = { 'info': 'prestamo', 'mensaje': f'Has pedido prestado el libro {libro.titulo} exitosamente.', 'libros': Libro.objects.all()}
            return render(request, 'lista_libros.html', datos)
    else:
        form = PrestamoForm(initial={'libros': [libro], 'solicitante': request.user})

    return render(request, 'prestamo.html', {'form': form, 'prestamo': None})

def manejar_actualizar_prestamo(request, prestamo_pk):
    prestamo = get_object_or_404(Prestamo, pk=prestamo_pk)
    if request.method == 'POST':
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            registrar_uso(request.user, f"Actualizó el préstamo para '{prestamo.libros.all().first().titulo}'", 'Prestamo')
            return redirect('lista-libros')
    else:
        form = PrestamoForm(instance=prestamo)

    return render(request, 'prestamo.html', {'form': form, 'prestamo': prestamo})

@login_required
def eliminar_prestamo(request, pk):
    if request.user.groups.filter(name='bibliotecario').exists():
        Prestamo.objects.filter(pk=pk).delete()
        accion = f"Eliminó el prestamo con id {pk}"
        registrar_uso(request.user, accion, 'Prestamo')
        return redirect('lista_prestamos')
    else:
        group_error = f"No tienes permisos para acceder a esta página."
        return render(request, 'index.html', {'group_error': group_error})

@login_required
def marcar_devuelto(request, pk):
    if request.user.groups.filter(name='bibliotecario').exists():
        prestamo = Prestamo.objects.get(pk=pk)
        prestamo.estado = 'Devuelto'
        prestamo.save()
        accion = f"Marcó como devuelto el préstamo con id {pk}"
        registrar_uso(request.user, accion, 'Prestamo')
        return redirect('prestamos')
    else:
        group_error = f"No tienes permisos para acceder a esta página."
        return render(request, 'index.html', {'group_error': group_error})

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
    if request.user.groups.filter(name='bibliotecario').exists():
        prestamos = Prestamo.objects.all().order_by('-fecha_prestamo')

        # Configuración de la paginación
        paginator = Paginator(prestamos, 10)
        page = request.GET.get('page')
        prestamos = paginator.get_page(page)

        return render(request, 'lista_prestamos.html', {'prestamos': prestamos})
    else:
        group_error = f"No tienes permisos para acceder a esta página."
        return render(request, 'index.html', {'group_error': group_error})

@login_required
def lista_historial(request):
    if request.user.groups.filter(name='bibliotecario').exists():
        # Obtiene todos los historiales y los ordena por fecha
        historiales_list = HistorialMovimientos.objects.all().order_by('-fecha')

        # Configuración de la paginación
        paginator = Paginator(historiales_list, 10) # Muestra 10 historiales por página
        page = request.GET.get('page')
        historiales = paginator.get_page(page)

        return render(request, 'historial.html', {'historiales': historiales})
    else:
        group_error = f"No tienes permisos para acceder a esta página."
        return render(request, 'index.html', {'group_error': group_error})
class DetallePrestamo(DetailView):
    model = Prestamo
    template_name = 'detalle_prestamo.html'

def registrar_uso(user, accion, tabla=None):
    # guardar en HistorialMovimientos
    datos = { 'usuario': user, 'accion': accion, 'tabla': tabla }
    HistorialMovimientos.objects.create(**datos)