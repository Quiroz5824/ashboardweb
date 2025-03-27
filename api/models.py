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
    residencia = models.CharField(max_length=255)
    trabaja = models.BooleanField(default=False)
    trabajo = models.CharField(max_length=255, null=True, blank=True)
    preparatoria = models.ForeignKey(Preparatoria, on_delete=models.SET_NULL, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ['id']

# Discapacidades del estudiante
class EstudianteDiscapacidad(models.Model):
    id = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    tipo_discapacidad = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Discapacidad del Estudiante"
        verbose_name_plural = "Discapacidades de Estudiantes"
        ordering = ['estudiante']

# Información laboral del estudiante
class EstudianteTrabajo(models.Model):
    id = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    tipo_trabajo = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Trabajo del Estudiante"
        verbose_name_plural = "Trabajos de Estudiantes"
        ordering = ['estudiante']

# Egresados
class Egresado(models.Model):
    id = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    fecha_egreso = models.DateField()

    class Meta:
        verbose_name = "Egresado"
        verbose_name_plural = "Egresados"
        ordering = ['fecha_egreso']

# Tiempo en finalizar estudios
class TiempoFinalizacion(models.Model):
    id = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField()
    duracion_carrera = models.IntegerField(help_text="Duración en meses")

    class Meta:
        verbose_name = "Tiempo de Finalización"
        verbose_name_plural = "Tiempos de Finalización"
        ordering = ['duracion_carrera']

# Motivos de abandono
class MotivoAbandono(models.Model):
    id = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    fecha_abandono = models.DateField()
    motivo = models.CharField(max_length=255)
    comentarios = models.TextField(blank=True)

    class Meta:
        verbose_name = "Motivo de Abandono"
        verbose_name_plural = "Motivos de Abandono"
        ordering = ['fecha_abandono']
# Docentes
class Docente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=255)
    especialidad = models.CharField(max_length=255)
    usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    materias = models.ManyToManyField('Materia', through='DocenteMateria')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"
        ordering = ['id']

# Materias
class Materia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    cuatrimestre = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"
        ordering = ['cuatrimestre']

# Relación Docente-Materia
class DocenteMateria(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Docente-Materia"
        verbose_name_plural = "Docentes-Materias"
        unique_together = ('docente', 'materia')

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

# Evaluación docente
class EvaluacionDocente(models.Model):
    id = models.AutoField(primary_key=True)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    fecha = models.DateField()
    puntuacion = models.DecimalField(max_digits=4, decimal_places=2)
    comentario = models.TextField(blank=True)

    class Meta:
        verbose_name = "Evaluación Docente"
        verbose_name_plural = "Evaluaciones Docentes"
        ordering = ['fecha']

# Distribución por edad
class DistribucionEdad(models.Model):
    id = models.AutoField(primary_key=True)
    edad = models.IntegerField()
    cantidad = models.IntegerField()
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Distribución por Edad"
        verbose_name_plural = "Distribuciones por Edad"
        ordering = ['edad', 'carrera']
        unique_together = ('edad', 'carrera')

# Distribución por residencia
class DistribucionResidencia(models.Model):
    id = models.AutoField(primary_key=True)
    residencia = models.CharField(max_length=255)
    coordenadas = models.CharField(max_length=100, null=True, blank=True)
    cantidad = models.IntegerField()

    class Meta:
        verbose_name = "Distribución por Residencia"
        verbose_name_plural = "Distribuciones por Residencia"
        ordering = ['residencia']

# Distribución por edad y carrera
class DistribucionEdadCarrera(models.Model):
    id = models.AutoField(primary_key=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    edad = models.IntegerField()
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.carrera.nombre} - {self.edad} años: {self.cantidad} estudiantes"

    class Meta:
        verbose_name = "Distribución Edad por Carrera"
        verbose_name_plural = "Distribuciones Edad por Carrera"
        ordering = ['carrera', 'edad']
        unique_together = ('carrera', 'edad')

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

