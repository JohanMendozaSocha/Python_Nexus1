from django.db import models
from django.conf import settings
 #Esto es para los datos, no hace nada mas.
class Foro(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Creador del Foro ligado al usuario
    id_creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <--- Este es el codigo q conecta a la tabla usuario.
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.titulo

class Publicacion(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Conexión obligatoria: A qué foro pertenece este mensaje
    id_foro = models.ForeignKey(Foro, on_delete=models.CASCADE)
    
    # Conexión obligatoria: Qué usuario escribió este mensaje
    id_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.titulo} por {self.id_usuario}"
    #Hasta aca