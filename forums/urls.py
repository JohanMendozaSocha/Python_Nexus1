from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_foros, name='forum_list'),
    path('create/', views.crear_foro, name='forum_create'),
    path('<int:foro_id>/', views.detalle_foro, name='forum_detail'),
    path('<int:foro_id>/delete/', views.eliminar_foro, name='forum_delete'),
    path('reply/<int:pub_id>/delete/', views.eliminar_publicacion, name='reply_delete'),
    path('report/', views.reportar_contenido, name='report_content'),
]
