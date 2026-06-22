from django.db import models
from django.contrib.auth.models import AbstractUser
    #Con esto usamos una tabla q Django ya trae por defecto, para no crear la tabla manualmente en MySQLWorkbench.
class Usuario(AbstractUser):
    #Django ya tiene por defecto: username, password, email, first_name, last_name.
    
    #Estos campos son para el avatar del usuario.
    estado = models.CharField(max_length=20, default='ACTIVO')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', null=True, blank=True)

    def __str__(self):
        return self.username