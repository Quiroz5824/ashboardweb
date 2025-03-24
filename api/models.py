
from django.db import models

class Usuarios(models.Model): 
    usuario_id = models.AutoField(primary_key=True)  
    matricula = models.CharField(max_length=20, unique=True)  
    password = models.CharField(max_length=255)  
    nombre = models.CharField(max_length=255)  

    def __str__(self):
        return f"{self.matricula} - {self.nombre}"
