from django.db import models
from django.contrib.auth.models import User

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"


class Editorial(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    numero_serie = models.CharField(max_length=100, unique=True)
    titulo = models.CharField(max_length=200)
    anio_publicacion = models.IntegerField()
    autores = models.ManyToManyField(Autor)
    categorias = models.ManyToManyField(Categoria)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class Prestamo(models.Model):
    libros = models.ManyToManyField(Libro)
    fecha_prestamo = models.DateField()
    fecha_devolucion_estimada = models.DateField()
    fecha_devolucion_real = models.DateField(null=True, blank=True)
    dias_retraso = models.IntegerField(default=0)
    multa = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    costo_prestamo = models.DecimalField(max_digits=6, decimal_places=2)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Prestamo a {self.solicitante.username} - {self.fecha_prestamo}"
    
class PerfilUsuario(models.Model):
    # Extender el modelo User para que posea campos adicionales
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username