from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list_view, name='event_list'),
    path('crear/', views.crear_evento, name='crear_evento'), 
    path('detalle/<int:pk>/', views.event_detail_view, name='event_detail'),
    path('unirse/<int:pk>/', views.unirse_evento, name='unirse_evento'),
    path('eliminar/<int:pk>/', views.eliminar_evento, name='eliminar_evento'),
    path('editar/<int:pk>/', views.editar_evento, name='editar_evento'),
    path('reportar/<int:pk>/', views.reportar_evento, name='reportar_evento'),
]