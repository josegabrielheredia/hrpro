from django.contrib import admin
from .models import Departamento, Empleado, Asistencia, Nomina, Candidato, Evaluacion


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'departamento', 'cargo', 'estado')
    search_fields = ('nombre', 'apellido', 'cedula', 'cargo')
    list_filter = ('departamento', 'estado')


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'fecha', 'hora_entrada', 'hora_salida', 'estado')
    search_fields = ('empleado__nombre', 'empleado__apellido')
    list_filter = ('estado',)


@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'fecha_pago', 'salario_base', 'bonificaciones', 'descuentos')
    search_fields = ('empleado__nombre', 'empleado__apellido')
    list_filter = ('fecha_pago',)


@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'puesto', 'estado', 'fecha_postulacion')
    search_fields = ('nombre', 'apellido', 'cedula', 'puesto')
    list_filter = ('estado',)


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('candidato', 'fecha', 'puntuacion', 'resultado')
    search_fields = ('candidato__nombre', 'candidato__apellido', 'resultado')
    list_filter = ('resultado',)
