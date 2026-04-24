import json

from django import forms

from .models import Asistencia, Candidato, Cargo, Departamento, Empleado, Evaluacion, Nomina


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
            if field_name == 'descripcion_nuevo_departamento':
                widget.attrs['placeholder'] = 'Descripcion opcional'
            if field_name == 'nuevo_cargo':
                widget.attrs['placeholder'] = 'Ejemplo: Analista de Datos'
            if field_name == 'descripcion_nuevo_cargo':
                widget.attrs['placeholder'] = 'Descripcion opcional'


class EmpleadoForm(StyledModelForm):
    nuevo_departamento = forms.CharField(
        required=False,
        label='Nuevo departamento',
        help_text='Si no existe, se crea y se asigna automaticamente al empleado.',
    )
    descripcion_nuevo_departamento = forms.CharField(
        required=False,
        label='Descripcion del nuevo departamento',
        widget=forms.Textarea(attrs={'rows': 2}),
    )
    nuevo_cargo = forms.CharField(
        required=False,
        label='Nuevo cargo',
        help_text='Si no existe, se crea y se asigna automaticamente al empleado.',
    )
    descripcion_nuevo_cargo = forms.CharField(
        required=False,
        label='Descripcion del nuevo cargo',
        widget=forms.Textarea(attrs={'rows': 2}),
    )

    class Meta:
        model = Empleado
        fields = [
            'nombre', 'apellido', 'cedula', 'departamento', 'nuevo_departamento',
            'descripcion_nuevo_departamento', 'cargo', 'nuevo_cargo', 'descripcion_nuevo_cargo',
            'sueldo_mensual_dop', 'email', 'telefono', 'fecha_ingreso',
            'estado', 'expediente'
        ]
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
            'expediente': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departamento'].queryset = Departamento.objects.order_by('nombre')
        self.fields['departamento'].empty_label = 'Selecciona un departamento'
        self.fields['cargo'].required = False

        cargo_choices = [('', 'Selecciona un cargo')]
        cargo_choices.extend([(cargo.nombre, cargo.nombre) for cargo in Cargo.objects.order_by('nombre')])

        if self.instance and self.instance.pk and self.instance.cargo:
            if not any(existing[0] == self.instance.cargo for existing in cargo_choices):
                cargo_choices.append((self.instance.cargo, self.instance.cargo))

        if self.is_bound:
            cargo_enviado = (self.data.get('cargo') or '').strip()
            if cargo_enviado and not any(existing[0] == cargo_enviado for existing in cargo_choices):
                cargo_choices.append((cargo_enviado, cargo_enviado))

        self.fields['cargo'].widget = forms.Select(choices=cargo_choices)
        self.fields['cargo'].widget.attrs['class'] = 'form-select'
        self.fields['cargo'].help_text = 'Selecciona un cargo existente o crea uno nuevo con el boton +.'
        self.fields['sueldo_mensual_dop'].label = 'Sueldo mensual (DOP)'
        self.fields['sueldo_mensual_dop'].widget.attrs.update({'step': '0.01', 'min': '0', 'inputmode': 'decimal'})
        self.fields['sueldo_mensual_dop'].help_text = 'Monto en pesos dominicanos (RD$).'

    def clean_nuevo_departamento(self):
        return self.cleaned_data.get('nuevo_departamento', '').strip()

    def clean_descripcion_nuevo_departamento(self):
        return self.cleaned_data.get('descripcion_nuevo_departamento', '').strip()

    def clean_sueldo_mensual_dop(self):
        sueldo = self.cleaned_data.get('sueldo_mensual_dop')
        if sueldo is not None and sueldo <= 0:
            raise forms.ValidationError('El sueldo mensual debe ser mayor que 0.')
        return sueldo

    def clean_nuevo_cargo(self):
        return self.cleaned_data.get('nuevo_cargo', '').strip()

    def clean_descripcion_nuevo_cargo(self):
        return self.cleaned_data.get('descripcion_nuevo_cargo', '').strip()

    def clean(self):
        cleaned_data = super().clean()
        cargo = (cleaned_data.get('cargo') or '').strip()
        nuevo_cargo = (cleaned_data.get('nuevo_cargo') or '').strip()

        if not cargo and not nuevo_cargo:
            self.add_error('cargo', 'Selecciona un cargo o crea uno nuevo.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        nuevo_departamento = self.cleaned_data.get('nuevo_departamento')
        descripcion_nuevo_departamento = self.cleaned_data.get('descripcion_nuevo_departamento', '')
        cargo_seleccionado = self.cleaned_data.get('cargo', '')
        nuevo_cargo = self.cleaned_data.get('nuevo_cargo', '')
        descripcion_nuevo_cargo = self.cleaned_data.get('descripcion_nuevo_cargo', '')

        if nuevo_departamento:
            departamento_existente = Departamento.objects.filter(nombre__iexact=nuevo_departamento).first()
            if departamento_existente:
                instance.departamento = departamento_existente
            else:
                instance.departamento = Departamento.objects.create(
                    nombre=nuevo_departamento,
                    descripcion=descripcion_nuevo_departamento,
                )

        if nuevo_cargo:
            cargo_existente = Cargo.objects.filter(nombre__iexact=nuevo_cargo).first()
            if cargo_existente:
                instance.cargo = cargo_existente.nombre
            else:
                cargo_creado = Cargo.objects.create(
                    nombre=nuevo_cargo,
                    descripcion=descripcion_nuevo_cargo,
                )
                instance.cargo = cargo_creado.nombre
        elif cargo_seleccionado:
            instance.cargo = cargo_seleccionado
            Cargo.objects.get_or_create(nombre=cargo_seleccionado)

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['salario_base'].required = False
        self.fields['salario_base'].label = 'Salario base (DOP)'
        self.fields['salario_base'].widget.attrs.update({'step': '0.01', 'min': '0', 'inputmode': 'decimal'})
        self.fields['salario_base'].help_text = 'Se completa con el sueldo del empleado si lo dejas vacio.'

        empleados = Empleado.objects.all().order_by('nombre', 'apellido')
        self.empleado_sueldo_map_json = json.dumps(
            {str(empleado.id): str(empleado.sueldo_mensual_dop) for empleado in empleados}
        )

        if not self.is_bound and not self.instance.pk:
            empleado_inicial = self.initial.get('empleado')
            if empleado_inicial:
                empleado = Empleado.objects.filter(pk=empleado_inicial).only('sueldo_mensual_dop').first()
                if empleado:
                    self.initial['salario_base'] = empleado.sueldo_mensual_dop

    def clean(self):
        cleaned_data = super().clean()
        empleado = cleaned_data.get('empleado')
        salario_base = cleaned_data.get('salario_base')

        if salario_base in (None, ''):
            if empleado:
                cleaned_data['salario_base'] = empleado.sueldo_mensual_dop
            else:
                self.add_error('salario_base', 'Selecciona un empleado para usar su sueldo por defecto.')

        return cleaned_data

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


class DepartamentoForm(StyledModelForm):
    class Meta:
        model = Departamento
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class CargoForm(StyledModelForm):
    class Meta:
        model = Cargo
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
