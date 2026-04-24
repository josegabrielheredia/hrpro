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

## Variables de entorno sugeridas
```bash
SECRET_KEY='tu_secreto_seguro'
DEBUG='False'
DATABASE_URL='postgres://usuario:pass@host:puerto/dbname'
ALLOWED_HOSTS='hrpro.onrender.com,localhost,127.0.0.1'
ADMIN_USERNAME='josegabriel'
ADMIN_EMAIL='admin@example.com'
ADMIN_PASSWORD='josegab0507W'
```

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
