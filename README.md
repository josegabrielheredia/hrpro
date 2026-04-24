# HRPro

Sistema de Gestión de Recursos Humanos construido con Django y PostgreSQL.

## Descripción
HRPro automatiza los procesos de empleados, asistencia, nómina, reclutamiento y reportes administrativos.

## Estructura del proyecto
- `hrpro/`: configuración del proyecto Django.
- `core/`: aplicación central con modelos, vistas, formularios y plantillas.
- `static/`: archivos CSS y JavaScript.
- `templates/`: plantillas compartidas.

## Requisitos
- Python 3.11+
- PostgreSQL (o usar la base de datos definida en `DATABASE_URL`)
- Variables de entorno:
  - `SECRET_KEY`
  - `DEBUG`
  - `DATABASE_URL`
  - `ALLOWED_HOSTS`

## Comandos locales
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Configuración de Render
- Build Command:
  - `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
- Start Command:
  - `gunicorn hrpro.wsgi:application`

> Nota: la base de datos del despliegue es independiente de tu entorno local. En producción puedes usar `ADMIN_USERNAME`/`ADMIN_EMAIL`/`ADMIN_PASSWORD` o los nombres estándar `DJANGO_SUPERUSER_USERNAME`/`DJANGO_SUPERUSER_EMAIL`/`DJANGO_SUPERUSER_PASSWORD`.

## Variables de entorno sugeridas
```bash
SECRET_KEY='tu_secreto_seguro'
DEBUG='False'
DATABASE_URL='postgres://usuario:pass@host:puerto/dbname'
ALLOWED_HOSTS='hrpro.onrender.com,localhost,127.0.0.1'
ADMIN_USERNAME='admin'
ADMIN_EMAIL='admin@example.com'
ADMIN_PASSWORD='cambia-esta-clave'
ADMIN_SETUP_ENABLED='False'
ADMIN_SETUP_KEY='clave-larga-y-unica'
DJANGO_SUPERUSER_USERNAME='admin'
DJANGO_SUPERUSER_EMAIL='admin@example.com'
DJANGO_SUPERUSER_PASSWORD='cambia-esta-clave'
```

## Ruta temporal para crear admin en produccion
- Endpoint: `POST /crear-admin-seguro/`
- Enviar `key` por `form-data` o `x-www-form-urlencoded`.
- Requiere: `ADMIN_SETUP_ENABLED=True` y `ADMIN_SETUP_KEY`.
- Despues de usarla, volver `ADMIN_SETUP_ENABLED=False`.

## Módulos incluidos
- Empleados
- Asistencia
- Nómina
- Reclutamiento
- Reportes
- Usuarios y seguridad

## Notas
- `STATIC_ROOT` está configurado para `staticfiles`.
- `whitenoise` sirve los archivos estáticos en producción.
- El proyecto funciona con PostgreSQL cuando `DATABASE_URL` está configurado.
