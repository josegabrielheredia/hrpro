from django import forms
from .models import Empleado, Asistencia, Nomina, Candidato, Evaluacion


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'nombre', 'apellido', 'cedula', 'departamento', 'cargo', 'email',
            'telefono', 'fecha_ingreso', 'estado', 'expediente'
        ]
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
            'expediente': forms.Textarea(attrs={'rows': 3}),
        }


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['empleado', 'fecha', 'hora_entrada', 'hora_salida', 'comentarios']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_entrada': forms.TimeInput(attrs={'type': 'time'}),
            'hora_salida': forms.TimeInput(attrs={'type': 'time'}),
            'comentarios': forms.Textarea(attrs={'rows': 2}),
        }


class NominaForm(forms.ModelForm):
    class Meta:
        model = Nomina
        fields = ['empleado', 'salario_base', 'bonificaciones', 'descuentos', 'fecha_pago', 'comentarios']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
            'comentarios': forms.Textarea(attrs={'rows': 2}),
        }


class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['nombre', 'apellido', 'cedula', 'email', 'telefono', 'puesto', 'estado']


class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['candidato', 'fecha', 'puntuacion', 'comentarios', 'resultado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'comentarios': forms.Textarea(attrs={'rows': 2}),
        }
