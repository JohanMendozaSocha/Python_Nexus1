from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('foros/', include('forums.urls')),
    path('eventos/', include('events.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

handler404 = 'forums.views.error_404_view'