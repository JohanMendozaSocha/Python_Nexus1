from django.urls import path
from . import views

urlpatterns = [
    # Ruta principal para el panel estilo Facebook
    path('', views.panel_eventos, name='panel_eventos'),
    # 🌟 NUEVA RUTA: Para la página del formulario de creación
    path('crear/', views.crear_evento, name='crear_evento'),
    
    # Rutas de acciones
    path('unirse/<int:pk>/', views.unirse_evento, name='unirse_evento'),
    path('eliminar/<int:pk>/', views.eliminar_evento, name='eliminar_evento'),
    path('editar/<int:pk>/', views.editar_evento, name='editar_evento'),
    path('reportar/<int:pk>/', views.reportar_evento, name='reportar_evento'),
]