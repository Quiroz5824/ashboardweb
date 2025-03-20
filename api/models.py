
from django.db import models

class Usuarios(models.Model): 
    usuario_id = models.AutoField(primary_key=True)  # ID automático
    matricula = models.CharField(max_length=20, unique=True)  # Matrícula única
    password = models.CharField(max_length=255)  # Contraseña
    nombre = models.CharField(max_length=255)  # Nombre completo (opcional)

    def __str__(self):
        return f"{self.matricula} - {self.nombre}"
