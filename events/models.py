from django.db import models
from django.conf import settings # Para poder jalar el usuario del sistema

    #Esto es para especificarle a Django la estructura de la tabla de eventos de nuestra base de datos,
    #para evitar errores en los campos ingresados

class Evento(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=255, null=True, blank=True)
    f_inicio = models.DateTimeField()
    f_fin = models.DateTimeField()
    categoria = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    #Relacion con el usuario (Creador del evento)
    id_creador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    #Para guardar quiénes se unen al evento (botón "Asistiré")
    asistentes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='eventos_asistidos', blank=True)
    def __str__(self):
        return self.titulo