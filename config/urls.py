from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),


    # Le decimos al jefe que cuando alguien busque "eventos/", 
    # vaya y mire el archivo urls.py interno de la app 'event'
    path('eventos/', include('events.urls')),
    
]