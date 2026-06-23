from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    
    # Incluye las rutas de la app de usuarios
    path('users/', include('users.urls')),
    
    # Redirección segura de la raíz del sitio al login
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
]