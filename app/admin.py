from django.contrib import admin
from .models import Libro, Autor, Editorial, Categoria

# Clase de personalización para el modelo Libro
class LibroAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista de objetos
    list_display = ('titulo', 'editorial', 'anio_publicacion')

    # Campos por los que se puede filtrar en la lista
    list_filter = ('editorial', 'anio_publicacion', 'categorias')

    # Campos por los que se puede buscar en la lista
    search_fields = ('titulo', 'autores__nombre')

    # Organizar los campos en la vista de detalle
    fieldsets = (
        (None, {
            'fields': ('titulo', 'autores', 'editorial')
        }),
        ('Información Adicional', {
            'fields': ('anio_publicacion', 'categorias'),
            'classes': ('collapse',),
        }),
    )

# Registra el modelo Libro con la personalización
admin.site.register(Libro, LibroAdmin)

# Registra otros modelos de manera normal
admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Categoria)