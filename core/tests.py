import os
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from .forms import EmpleadoForm, NominaForm
from .models import Cargo, Departamento, Empleado


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


class EmpleadoFormDepartamentoTests(TestCase):
    def test_crea_departamento_nuevo_si_no_existe(self):
        form = EmpleadoForm(data={
            'nombre': 'Ana',
            'apellido': 'Lopez',
            'cedula': '001-0000000-1',
            'departamento': '',
            'cargo': 'Analista',
            'email': 'ana@example.com',
            'telefono': '8090000001',
            'fecha_ingreso': '2026-04-24',
            'estado': 'ACTIVO',
            'expediente': '',
            'nuevo_departamento': 'Tecnologia',
            'descripcion_nuevo_departamento': '',
            'nuevo_cargo': '',
            'descripcion_nuevo_cargo': '',
            'sueldo_mensual_dop': '45000.00',
        })

        self.assertTrue(form.is_valid(), form.errors)
        empleado = form.save()
        self.assertEqual(empleado.departamento.nombre, 'Tecnologia')
        self.assertEqual(Departamento.objects.filter(nombre='Tecnologia').count(), 1)

    def test_reutiliza_departamento_existente_sin_duplicar(self):
        departamento = Departamento.objects.create(nombre='Finanzas')

        form = EmpleadoForm(data={
            'nombre': 'Luis',
            'apellido': 'Garcia',
            'cedula': '001-0000000-2',
            'departamento': '',
            'cargo': 'Contador',
            'email': 'luis@example.com',
            'telefono': '8090000002',
            'fecha_ingreso': '2026-04-24',
            'estado': 'ACTIVO',
            'expediente': '',
            'nuevo_departamento': 'finanzas',
            'descripcion_nuevo_departamento': '',
            'nuevo_cargo': '',
            'descripcion_nuevo_cargo': '',
            'sueldo_mensual_dop': '52000.00',
        })

        self.assertTrue(form.is_valid(), form.errors)
        empleado = form.save()

        self.assertEqual(empleado.departamento.id, departamento.id)
        self.assertEqual(Departamento.objects.filter(nombre__iexact='finanzas').count(), 1)
        self.assertTrue(Empleado.objects.filter(id=empleado.id).exists())

    def test_usa_departamento_existente_seleccionado(self):
        departamento = Departamento.objects.create(nombre='Operaciones')

        form = EmpleadoForm(data={
            'nombre': 'Maria',
            'apellido': 'Perez',
            'cedula': '001-0000000-3',
            'departamento': str(departamento.id),
            'cargo': 'Supervisor',
            'email': 'maria@example.com',
            'telefono': '8090000003',
            'fecha_ingreso': '2026-04-24',
            'estado': 'ACTIVO',
            'expediente': '',
            'nuevo_departamento': '',
            'descripcion_nuevo_departamento': '',
            'nuevo_cargo': '',
            'descripcion_nuevo_cargo': '',
            'sueldo_mensual_dop': '61000.00',
        })

        self.assertTrue(form.is_valid(), form.errors)
        empleado = form.save()
        self.assertEqual(empleado.departamento.id, departamento.id)

    def test_guarda_descripcion_cuando_crea_departamento_nuevo(self):
        form = EmpleadoForm(data={
            'nombre': 'Pedro',
            'apellido': 'Sanchez',
            'cedula': '001-0000000-4',
            'departamento': '',
            'cargo': 'Coordinador',
            'email': 'pedro@example.com',
            'telefono': '8090000004',
            'fecha_ingreso': '2026-04-24',
            'estado': 'ACTIVO',
            'expediente': '',
            'nuevo_departamento': 'Compras',
            'descripcion_nuevo_departamento': 'Gestion de adquisiciones y proveedores.',
            'nuevo_cargo': '',
            'descripcion_nuevo_cargo': '',
            'sueldo_mensual_dop': '48000.00',
        })

        self.assertTrue(form.is_valid(), form.errors)
        empleado = form.save()
        self.assertEqual(empleado.departamento.nombre, 'Compras')
        self.assertEqual(empleado.departamento.descripcion, 'Gestion de adquisiciones y proveedores.')

    def test_crea_cargo_nuevo_si_no_existe(self):
        form = EmpleadoForm(data={
            'nombre': 'Elena',
            'apellido': 'Diaz',
            'cedula': '001-0000000-5',
            'departamento': '',
            'cargo': '',
            'email': 'elena@example.com',
            'telefono': '8090000005',
            'fecha_ingreso': '2026-04-24',
            'estado': 'ACTIVO',
            'expediente': '',
            'nuevo_departamento': '',
            'descripcion_nuevo_departamento': '',
            'nuevo_cargo': 'Gerente de Proyecto',
            'descripcion_nuevo_cargo': 'Lidera proyectos de tecnologia.',
            'sueldo_mensual_dop': '95000.00',
        })

        self.assertTrue(form.is_valid(), form.errors)
        empleado = form.save()
        self.assertEqual(empleado.cargo, 'Gerente de Proyecto')
        self.assertTrue(Cargo.objects.filter(nombre='Gerente de Proyecto').exists())

    def test_usa_cargo_existente_y_no_duplica(self):
        Cargo.objects.create(nombre='Reclutador')

        form = EmpleadoForm(data={
            'nombre': 'Jose',
            'apellido': 'Ruiz',
            'cedula': '001-0000000-6',
            'departamento': '',
            'cargo': 'Reclutador',
            'email': 'jose@example.com',
            'telefono': '8090000006',
            'fecha_ingreso': '2026-04-24',
            'estado': 'ACTIVO',
            'expediente': '',
            'nuevo_departamento': '',
            'descripcion_nuevo_departamento': '',
            'nuevo_cargo': '',
            'descripcion_nuevo_cargo': '',
            'sueldo_mensual_dop': '55000.00',
        })

        self.assertTrue(form.is_valid(), form.errors)
        empleado = form.save()
        self.assertEqual(empleado.cargo, 'Reclutador')
        self.assertEqual(Cargo.objects.filter(nombre='Reclutador').count(), 1)

    def test_rechaza_sueldo_cero_o_negativo(self):
        form = EmpleadoForm(data={
            'nombre': 'Lina',
            'apellido': 'Martinez',
            'cedula': '001-0000000-7',
            'departamento': '',
            'cargo': 'Asistente',
            'email': 'lina@example.com',
            'telefono': '8090000007',
            'fecha_ingreso': '2026-04-24',
            'estado': 'ACTIVO',
            'expediente': '',
            'nuevo_departamento': '',
            'descripcion_nuevo_departamento': '',
            'nuevo_cargo': '',
            'descripcion_nuevo_cargo': '',
            'sueldo_mensual_dop': '0',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('sueldo_mensual_dop', form.errors)


class NominaFormDefaultsTests(TestCase):
    def test_usa_sueldo_del_empleado_si_salario_base_vacio(self):
        empleado = Empleado.objects.create(
            nombre='Sara',
            apellido='Gomez',
            cedula='001-0000001-1',
            cargo='Analista',
            sueldo_mensual_dop='68000.00',
            fecha_ingreso='2026-04-24',
            estado='ACTIVO',
        )

        form = NominaForm(data={
            'empleado': empleado.id,
            'salario_base': '',
            'bonificaciones': '0',
            'descuentos': '0',
            'fecha_pago': '2026-04-30',
            'comentarios': '',
        })

        self.assertTrue(form.is_valid(), form.errors)
        nomina = form.save()
        self.assertEqual(str(nomina.salario_base), '68000.00')

    def test_mapa_de_sueldos_incluye_empleados(self):
        empleado = Empleado.objects.create(
            nombre='Mario',
            apellido='Lopez',
            cedula='001-0000001-2',
            cargo='Supervisor',
            sueldo_mensual_dop='72000.00',
            fecha_ingreso='2026-04-24',
            estado='ACTIVO',
        )

        form = NominaForm()
        self.assertIn(str(empleado.id), form.empleado_sueldo_map_json)
