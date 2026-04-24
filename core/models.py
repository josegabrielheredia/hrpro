from datetime import time
from django.db import models


class Departamento(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('SUSPENDIDO', 'Suspendido'),
    ]

    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)
    cedula = models.CharField(max_length=20, unique=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    cargo = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    fecha_ingreso = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    expediente = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Asistencia(models.Model):
    ESTADO_ASISTENCIA = [
        ('PRESENTE', 'Presente'),
        ('TARDANZA', 'Tardanza'),
        ('AUSENTE', 'Ausente'),
    ]

    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField(null=True, blank=True)
    puntualidad = models.BooleanField(default=True)
    estado = models.CharField(max_length=20, choices=ESTADO_ASISTENCIA, default='PRESENTE')
    comentarios = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

    def save(self, *args, **kwargs):
        if self.hora_entrada and self.hora_entrada > time(9, 0):
            self.puntualidad = False
            self.estado = 'TARDANZA'
        elif self.hora_entrada:
            self.puntualidad = True
            self.estado = 'PRESENTE'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.empleado} - {self.fecha.strftime("%Y-%m-%d")}'


class Nomina(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    bonificaciones = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuentos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_pago = models.DateField()
    comentarios = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha_pago']
        verbose_name = 'Nómina'
        verbose_name_plural = 'Nóminas'

    def total_pago(self):
        return self.salario_base + self.bonificaciones - self.descuentos

    def __str__(self):
        return f'Nómina {self.empleado} - {self.fecha_pago}'


class Candidato(models.Model):
    ESTADO_CANDIDATO = [
        ('NUEVO', 'Nuevo'),
        ('EN_PROCESO', 'En proceso'),
        ('RECHAZADO', 'Rechazado'),
        ('CONTRATADO', 'Contratado'),
    ]

    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)
    cedula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    puesto = models.CharField(max_length=120)
    estado = models.CharField(max_length=20, choices=ESTADO_CANDIDATO, default='NUEVO')
    fecha_postulacion = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_postulacion']
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Evaluacion(models.Model):
    RESULTADO = [
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('PENDIENTE', 'Pendiente'),
    ]

    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='evaluaciones')
    fecha = models.DateField()
    puntuacion = models.PositiveIntegerField()
    comentarios = models.TextField(blank=True)
    resultado = models.CharField(max_length=20, choices=RESULTADO, default='PENDIENTE')

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'

    def __str__(self):
        return f'Evaluación {self.candidato} - {self.resultado}'
