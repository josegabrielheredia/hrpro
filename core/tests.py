import os
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase


class CrearAdminSeguroViewTests(TestCase):
    url = '/crear-admin-seguro/'

    def _base_env(self):
        return {
            'ADMIN_SETUP_ENABLED': 'True',
            'ADMIN_SETUP_KEY': 'test-key',
            'DJANGO_SUPERUSER_USERNAME': 'admin',
            'DJANGO_SUPERUSER_EMAIL': 'admin@example.com',
            'DJANGO_SUPERUSER_PASSWORD': 'ClaveFuerte12345',
        }

    @patch.dict(os.environ, {}, clear=False)
    def test_rejects_non_post_method(self):
        response = self.client.get(self.url, {'key': 'test-key'}, secure=True)
        self.assertEqual(response.status_code, 405)

    @patch.dict(os.environ, {}, clear=False)
    def test_rejects_invalid_key(self):
        with patch.dict(os.environ, self._base_env(), clear=False):
            response = self.client.post(self.url, {'key': 'wrong-key'}, secure=True)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content.decode(), 'Clave invalida')

    @patch.dict(os.environ, {}, clear=False)
    def test_returns_exists_when_superuser_already_exists(self):
        with patch.dict(os.environ, self._base_env(), clear=False):
            User.objects.create_superuser('admin', 'admin@example.com', 'ClaveFuerte12345')
            response = self.client.post(self.url, {'key': 'test-key'}, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'El superusuario ya existe')

    @patch.dict(os.environ, {}, clear=False)
    def test_creates_superuser_when_valid_request(self):
        with patch.dict(os.environ, self._base_env(), clear=False):
            response = self.client.post(self.url, {'key': 'test-key'}, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'Superusuario creado correctamente')
        self.assertTrue(User.objects.filter(username='admin', is_superuser=True).exists())
