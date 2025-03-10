from django.db import models

# Create your models here.
class Usuarios (models.Model): 
    usuario_id = models.AutoField(primary_key=True) 
    nombre_usuario= models.CharField(max_length=255)