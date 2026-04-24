from django import forms

from .models import Asistencia, Candidato, Departamento, Empleado, Evaluacion, Nomina


class StyledModelForm(forms.ModelForm):
    """Apply a consistent Bootstrap style across all project forms."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            current_class = widget.attrs.get('class', '').strip()

            if isinstance(widget, (forms.Select, forms.SelectMultiple)):
                base_class = 'form-select'
            elif isinstance(widget, forms.CheckboxInput):
                base_class = 'form-check-input'
            else:
                base_class = 'form-control'

            widget.attrs['class'] = f'{current_class} {base_class}'.strip()

            if field.required:
                widget.attrs['required'] = 'required'

            if field_name == 'nuevo_departamento':
                widget.attrs['placeholder'] = 'Ejemplo: Tecnologia'


class EmpleadoForm(StyledModelForm):
    nuevo_departamento = forms.CharField(
        required=False,
        label='Nuevo departamento',
        help_text='Si no existe, se crea y se asigna automaticamente al empleado.',
    )

    class Meta:
        model = Empleado
        fields = [
            'nombre', 'apellido', 'cedula', 'departamento', 'nuevo_departamento',
            'cargo', 'email', 'telefono', 'fecha_ingreso', 'estado', 'expediente'
        ]
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
            'expediente': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departamento'].queryset = Departamento.objects.order_by('nombre')
        self.fields['departamento'].empty_label = 'Selecciona un departamento'

    def clean_nuevo_departamento(self):
        return self.cleaned_data.get('nuevo_departamento', '').strip()

    def save(self, commit=True):
        instance = super().save(commit=False)
        nuevo_departamento = self.cleaned_data.get('nuevo_departamento')

        if nuevo_departamento:
            departamento_existente = Departamento.objects.filter(nombre__iexact=nuevo_departamento).first()
            if departamento_existente:
                instance.departamento = departamento_existente
            else:
                instance.departamento = Departamento.objects.create(nombre=nuevo_departamento)

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class AsistenciaForm(StyledModelForm):
    class Meta:
        model = Asistencia
        fields = ['empleado', 'fecha', 'hora_entrada', 'hora_salida', 'comentarios']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_entrada': forms.TimeInput(attrs={'type': 'time'}),
            'hora_salida': forms.TimeInput(attrs={'type': 'time'}),
            'comentarios': forms.Textarea(attrs={'rows': 2}),
        }


class NominaForm(StyledModelForm):
    class Meta:
        model = Nomina
        fields = ['empleado', 'salario_base', 'bonificaciones', 'descuentos', 'fecha_pago', 'comentarios']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
            'comentarios': forms.Textarea(attrs={'rows': 2}),
        }


class CandidatoForm(StyledModelForm):
    class Meta:
        model = Candidato
        fields = ['nombre', 'apellido', 'cedula', 'email', 'telefono', 'puesto', 'estado']


class EvaluacionForm(StyledModelForm):
    class Meta:
        model = Evaluacion
        fields = ['candidato', 'fecha', 'puntuacion', 'comentarios', 'resultado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'comentarios': forms.Textarea(attrs={'rows': 2}),
        }
