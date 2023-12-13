# Manual de Instalación BibliotecApp

## Requisitos del Sistema

- Sistema Operativo: Windows o Linux.
- Memoria: Al menos 2GB.
- Almacenamiento: Se recomiendan como mínimo 500 MB para la instalación. Posteriormente este aumentará según el uso que tenga el sistema de archivos (imágenes y base de datos).

## Entorno de Desarrollo

- Python: Versión 3.11.5.
- Django: Versión 4.2.7.
- Bases de Datos Compatible: MySQL.

## Instalación de Dependencias

1. Clona el repositorio: `git clone https://github.com/TecoMadriaga/bibliotecapp`
2. Navega al directorio del proyecto: `cd bibliotecapp`.
3. Instala las librerías necesarias: 

```
pip install pymysql mysqlclient pillow
```

## Configuración del Proyecto

- Cambia `ALLOWED_HOSTS = []` con el dominio correspondiente.
- Configura la base de datos en `settings.py`.
- Crea un superusuario.
- Desde la administración de Python, crea un nuevo grupo `Bibliotecarios` y asigna tanto al superusuario como al staff correspondiente ahí.

## Migraciones de la Base de Datos

- Ejecuta `python manage.py migrate` para realizar las migraciones necesarias.

## Ejecución del Servidor de Desarrollo

- Inicia el servidor con `python manage.py runserver`.

## Pruebas

- Puedes ingresar tanto libros como prestamos desde la misma web, teniendo las configuraciones realizadas.

## Problemas Comunes y Soluciones

- No se muestran las imágenes correctamente: Verifica que el path esté correcto desde `settings.py`.
