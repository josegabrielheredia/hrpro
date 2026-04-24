import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AsistenciaForm, CandidatoForm, EmpleadoForm, NominaForm
from .models import Asistencia, Candidato, Empleado, Nomina


def crear_admin_seguro(request):
    if request.method != 'POST':
        return HttpResponse('Metodo no permitido', status=405)

    setup_enabled = os.environ.get('ADMIN_SETUP_ENABLED', 'False').lower() in ('1', 'true', 'yes', 'on')
    if not setup_enabled:
        return HttpResponse('Ruta deshabilitada', status=404)

    admin_setup_key = os.environ.get('ADMIN_SETUP_KEY')
    provided_key = request.POST.get('key') or request.headers.get('X-Admin-Setup-Key')
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    if not admin_setup_key or not provided_key or provided_key != admin_setup_key:
        return HttpResponse('Clave invalida', status=403)

    if not username or not password:
        return HttpResponse('Falta configurar DJANGO_SUPERUSER_USERNAME o DJANGO_SUPERUSER_PASSWORD', status=500)

    if User.objects.filter(username=username).exists():
        return HttpResponse('El superusuario ya existe')

    User.objects.create_superuser(username, email, password)
    return HttpResponse('Superusuario creado correctamente')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Bienvenido al panel HRPro.')
            return redirect('dashboard')
        messages.error(request, 'Credenciales incorrectas. Intenta de nuevo.')

    return render(request, 'core/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


@login_required
def dashboard(request):
    empleados = Empleado.objects.count()
    asistencias = Asistencia.objects.count()
    nominas = Nomina.objects.count()
    candidatos = Candidato.objects.count()

    resumen = {
        'empleados': empleados,
        'asistencias': asistencias,
        'nominas': nominas,
        'candidatos': candidatos,
    }
    reciente_empleados = Empleado.objects.all()[:5]
    reciente_asistencias = Asistencia.objects.all()[:5]
    return render(request, 'core/dashboard.html', {
        'resumen': resumen,
        'reciente_empleados': reciente_empleados,
        'reciente_asistencias': reciente_asistencias,
    })


@login_required
def empleado_list(request):
    query = request.GET.get('q', '')
    empleados = Empleado.objects.all()
    if query:
        empleados = empleados.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(cedula__icontains=query)
        )
    return render(request, 'core/employee_list.html', {'empleados': empleados, 'query': query})


@login_required
def empleado_create(request):
    form = EmpleadoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Empleado registrado con éxito.')
        return redirect('empleado_list')
    return render(request, 'core/employee_form.html', {'form': form, 'title': 'Registrar empleado'})


@login_required
def empleado_edit(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    form = EmpleadoForm(request.POST or None, instance=empleado)
    if form.is_valid():
        form.save()
        messages.success(request, 'Empleado actualizado correctamente.')
        return redirect('empleado_list')
    return render(request, 'core/employee_form.html', {'form': form, 'title': 'Editar empleado'})


@login_required
def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado correctamente.')
        return redirect('empleado_list')
    return render(request, 'core/employee_detail.html', {'empleado': empleado, 'confirm_delete': True})


@login_required
def empleado_detail(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    historial = Asistencia.objects.filter(empleado=empleado).order_by('-fecha')[:10]
    return render(request, 'core/employee_detail.html', {'empleado': empleado, 'historial': historial})


@login_required
def asistencia_list(request):
    query = request.GET.get('q', '')
    asistencias = Asistencia.objects.select_related('empleado').all()
    if query:
        asistencias = asistencias.filter(
            Q(empleado__nombre__icontains=query) |
            Q(empleado__apellido__icontains=query) |
            Q(empleado__cedula__icontains=query)
        )
    return render(request, 'core/attendance_list.html', {'asistencias': asistencias, 'query': query})


@login_required
def asistencia_create(request):
    form = AsistenciaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Registro de asistencia guardado.')
        return redirect('asistencia_list')
    return render(request, 'core/attendance_form.html', {'form': form, 'title': 'Registrar asistencia'})


@login_required
def asistencia_edit(request, pk):
    asistencia = get_object_or_404(Asistencia, pk=pk)
    form = AsistenciaForm(request.POST or None, instance=asistencia)
    if form.is_valid():
        form.save()
        messages.success(request, 'Asistencia actualizada.')
        return redirect('asistencia_list')
    return render(request, 'core/attendance_form.html', {'form': form, 'title': 'Editar asistencia'})


@login_required
def asistencia_delete(request, pk):
    asistencia = get_object_or_404(Asistencia, pk=pk)
    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada.')
        return redirect('asistencia_list')
    return render(request, 'core/attendance_form.html', {'form': None, 'title': 'Eliminar asistencia', 'object': asistencia})


@login_required
def nomina_list(request):
    query = request.GET.get('q', '')
    nominas = Nomina.objects.select_related('empleado').all()
    if query:
        nominas = nominas.filter(
            Q(empleado__nombre__icontains=query) |
            Q(empleado__apellido__icontains=query) |
            Q(empleado__cedula__icontains=query)
        )
    return render(request, 'core/payroll_list.html', {'nominas': nominas, 'query': query})


@login_required
def nomina_create(request):
    form = NominaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Registro de nómina creado.')
        return redirect('nomina_list')
    return render(request, 'core/payroll_form.html', {'form': form, 'title': 'Registrar nómina'})


@login_required
def nomina_edit(request, pk):
    nomina = get_object_or_404(Nomina, pk=pk)
    form = NominaForm(request.POST or None, instance=nomina)
    if form.is_valid():
        form.save()
        messages.success(request, 'Nómina actualizada.')
        return redirect('nomina_list')
    return render(request, 'core/payroll_form.html', {'form': form, 'title': 'Editar nómina'})


@login_required
def nomina_delete(request, pk):
    nomina = get_object_or_404(Nomina, pk=pk)
    if request.method == 'POST':
        nomina.delete()
        messages.success(request, 'Nómina eliminada.')
        return redirect('nomina_list')
    return render(request, 'core/payroll_form.html', {'form': None, 'title': 'Eliminar nómina', 'object': nomina})


@login_required
def candidato_list(request):
    query = request.GET.get('q', '')
    candidatos = Candidato.objects.all()
    if query:
        candidatos = candidatos.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(cedula__icontains=query) |
            Q(puesto__icontains=query)
        )
    return render(request, 'core/candidate_list.html', {'candidatos': candidatos, 'query': query})


@login_required
def candidato_create(request):
    form = CandidatoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Candidato registrado.')
        return redirect('candidato_list')
    return render(request, 'core/candidate_form.html', {'form': form, 'title': 'Registrar candidato'})


@login_required
def candidato_edit(request, pk):
    candidato = get_object_or_404(Candidato, pk=pk)
    form = CandidatoForm(request.POST or None, instance=candidato)
    if form.is_valid():
        form.save()
        messages.success(request, 'Candidato actualizado.')
        return redirect('candidato_list')
    return render(request, 'core/candidate_form.html', {'form': form, 'title': 'Editar candidato'})


@login_required
def candidato_delete(request, pk):
    candidato = get_object_or_404(Candidato, pk=pk)
    if request.method == 'POST':
        candidato.delete()
        messages.success(request, 'Candidato eliminado.')
        return redirect('candidato_list')
    return render(request, 'core/candidate_form.html', {'form': None, 'title': 'Eliminar candidato', 'object': candidato})


@login_required
def reportes(request):
    empleados = Empleado.objects.count()
    asistencias = Asistencia.objects.count()
    nominas = Nomina.objects.count()
    candidatos = Candidato.objects.count()
    asistencias_ultimas = Asistencia.objects.select_related('empleado').all()[:10]
    nominas_ultimas = Nomina.objects.select_related('empleado').all()[:10]
    candidatos_ultimos = Candidato.objects.all()[:10]
    return render(request, 'core/report.html', {
        'empleados': empleados,
        'asistencias': asistencias,
        'nominas': nominas,
        'candidatos': candidatos,
        'asistencias_ultimas': asistencias_ultimas,
        'nominas_ultimas': nominas_ultimas,
        'candidatos_ultimos': candidatos_ultimos,
    })
