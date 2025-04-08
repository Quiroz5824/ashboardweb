from django.db import models


class Usuarios(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.matricula} - {self.nombre}"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['usuario_id']

# Carreras universitarias
class Carrera(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"
        ordering = ['id']

# Preparatorias de origen
class Preparatoria(models.Model):
    TIPO_CHOICES = [
        ('Bachillerato', 'Bachillerato'),
        ('Tecnica', 'Técnica'),
        ('Oficial', 'Oficial'),
        ('Tecnologico', 'Tecnológico'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Preparatoria"
        verbose_name_plural = "Preparatorias"
        ordering = ['id']

# Periodos escolares
class Periodo(models.Model):
    TIPO_CHOICES = [
        ('Cuatrimestre', 'Cuatrimestre'),
        ('Anual', 'Anual'),
    ]

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    anio = models.IntegerField()
    numero = models.IntegerField(help_text="Número de cuatrimestre o año (1, 2, 3, ...)")

    def __str__(self):
        return f"{self.tipo} {self.numero} - {self.anio}"

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"
        ordering = ['anio', 'numero']
        unique_together = ('tipo', 'anio', 'numero')

# Estudiantes
class Estudiante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')])
    preparatoria = models.ForeignKey(Preparatoria, on_delete=models.SET_NULL, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ['id']


class CreditosEstudiantePeriodo(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    creditos_aprobados = models.IntegerField()

    class Meta:
        unique_together = ('estudiante', 'periodo')
        verbose_name = "Créditos por Estudiante y Periodo"
        verbose_name_plural = "Créditos por Estudiante y Periodo"
        ordering = ['estudiante', 'periodo']

    def __str__(self):
        return f"{self.estudiante} - {self.periodo}: {self.creditos_aprobados} créditos"


# Egresados
class Egresado(models.Model):
    id = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    fecha_egreso = models.DateField()

    class Meta:
        verbose_name = "Egresado"
        verbose_name_plural = "Egresados"
        ordering = ['fecha_egreso']



# Materias
class Materia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    cuatrimestre = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"
        ordering = ['cuatrimestre']


# Grupos académicos
class Grupo(models.Model):
    id = models.AutoField(primary_key=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    cuatrimestre = models.IntegerField()
    turno = models.CharField(max_length=20, choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino')])

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
        ordering = ['carrera', 'cuatrimestre']

# Evaluaciones individuales
class Evaluacion(models.Model):
    id = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    calificacion = models.DecimalField(max_digits=4, decimal_places=2)
    fecha = models.DateField()

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        ordering = ['fecha']

# Resumen de evaluaciones por estudiante y periodo
class EvaluacionResumen(models.Model):
    id = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    cuatrimestre = models.IntegerField()
    anio = models.IntegerField()
    calificaciones = models.DecimalField(max_digits=4, decimal_places=2)
    aprobados = models.IntegerField()
    reprobados = models.IntegerField()
    promedio_cuatrimestral = models.DecimalField(max_digits=4, decimal_places=2)
    promedio_anual = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = "Evaluación Resumen"
        verbose_name_plural = "Evaluaciones Resumen"
        ordering = ['estudiante', 'periodo']

# Distribución por cuatrimestre y carrera
class DistribucionEstudiantesCuatrimestre(models.Model):
    id = models.AutoField(primary_key=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.carrera.nombre} - {self.periodo}: {self.cantidad} estudiantes"

    class Meta:
        verbose_name = "Distribución Estudiantes por Cuatrimestre"
        verbose_name_plural = "Distribuciones Estudiantes por Cuatrimestre"
        ordering = ['carrera', 'periodo']
        unique_together = ('carrera', 'periodo')

