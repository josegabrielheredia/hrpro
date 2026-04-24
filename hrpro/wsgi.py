import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrpro.settings')
application = get_wsgi_application()

try:
    from django.contrib.auth import get_user_model

    User = get_user_model()
    admin_username = os.getenv('ADMIN_USERNAME')
    admin_password = os.getenv('ADMIN_PASSWORD')
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')

    if admin_username and admin_password:
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(admin_username, admin_email, admin_password)
except Exception:
    pass
