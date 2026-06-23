from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from django.views.generic import RedirectView
=======
>>>>>>> c54ecee7ed5c33ae2922d8ed66257e48848ea161

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    
    # Incluye las rutas de la app de usuarios
    path('users/', include('users.urls')),
    
    # Redirección segura de la raíz del sitio al login
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
]
=======
    path('foros/', include('forums.urls')),
]
>>>>>>> c54ecee7ed5c33ae2922d8ed66257e48848ea161
