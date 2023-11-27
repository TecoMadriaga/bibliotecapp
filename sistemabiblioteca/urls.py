from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('historial/', views.lista_historial, name='historial'),
    path('libros/', views.lista_libros, name='lista-libros'),
    path('libros/<int:pk>', views.DetalleLibro.as_view(), name='detalle-libro'),
    path('libros/crear/', views.crear_libro, name='add-libro'),
    path('libros/editar/<int:pk>', views.editar_libro, name='edit-libro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name="logout"),
    path('marcar_devuelto/<int:pk>', views.marcar_devuelto, name='marcar-devuelto'),
    path('mis_prestamos/', views.lista_prestamos, name='mis-prestamos'),
    path('prestamo/actualizar/<int:pk>', views.manejar_prestamo, name='actualizar-prestamo'),
    path('prestamo/nuevo/<int:pk>', views.manejar_prestamo, name='nuevo-prestamo'),
    path('prestamos/', views.lista_todos_prestamos, name='prestamos'),
    path('signup/', views.RegistroUsuario.as_view(), name='signup'),
    path('user_login/', views.user_login, name='user-login'),
    path('user_logout/', views.user_logout, name='user-logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
