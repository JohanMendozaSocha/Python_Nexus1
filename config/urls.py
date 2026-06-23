from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD


    # Le decimos al jefe que cuando alguien busque "eventos/", 
    # vaya y mire el archivo urls.py interno de la app 'event'
    path('eventos/', include('events.urls')),
    
]
=======
    path('foros/', include('forums.urls')),
]
>>>>>>> c54ecee7ed5c33ae2922d8ed66257e48848ea161
