from django.db import models
from django.conf import settings

class Foro(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100, null=True, blank=True)
    # CORREGIDO: Ahora usa upload_to
    imagen = models.ImageField(upload_to="forum_covers/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    id_creador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.titulo

class Publicacion(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
   
    imagen = models.ImageField(upload_to="reply_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    id_foro = models.ForeignKey(Foro, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.titulo} por {self.id_usuario}"
    
class Reporte(models.Model):
  
     MOTIVOS = [
        ('SPAM', 'Spam / Advertising'),
        ('HARASSMENT', 'Harassment / Hate speech'),
        ('INAPPROPRIATE', 'Inappropriate content'),
        ('OTHER', 'Other'),

    ]
    
     motivo = models.CharField(max_length=20, choices = MOTIVOS, default='OTHER')
     comentario_adicional = models.TextField(blank=True, null=True)
     created_at = models.DateTimeField(auto_now_add=True)
    
    
     id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    
     id_foro = models.ForeignKey(Foro, on_delete=models.CASCADE, null=True, blank=True)
     id_publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, null=True, blank=True)

     def __str__(self):
        tipo = f"Forum: {self.id_foro.titulo}" if self.id_foro else f"Comment: {self.id_publicacion.id}"
        return f"Report by {self.id_usuario} on {tipo}"