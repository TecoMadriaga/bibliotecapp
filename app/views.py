from django.shortcuts import render
from app.models import Libro, Prestamo, PerfilUsuario

def index(request):
    return render(request, "index.html")
