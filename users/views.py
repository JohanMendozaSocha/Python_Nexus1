from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from events.models import Evento
from forums.models import Foro

from .models import Usuario


def login_view(request):

    if request.method == 'POST':

        usuario = request.POST.get('username')
        clave = request.POST.get('password')

        user = authenticate(
            request,
            username=usuario,
            password=clave
        )

        if user is not None:

            auth_login(request, user)

            messages.success(
                request,
                f"¡Bienvenido {user.username}!"
            )

            return redirect('dashboard')

        else:

            messages.error(
                request,
                "Usuario o contraseña incorrectos."
            )

            return redirect('login')

    return render(request, 'login.html')


def register_view(request):

    if request.method == 'POST':

        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')

        usuario = request.POST.get('username')
        correo = request.POST.get('email')

        clave = request.POST.get('password')
        confirmar_clave = request.POST.get('confirm_password')

        if clave != confirmar_clave:

            messages.error(
                request,
                "Las contraseñas no coinciden."
            )

            return redirect('register')

        if Usuario.objects.filter(username=usuario).exists():

            messages.error(
                request,
                "El nombre de usuario ya existe."
            )

            return redirect('register')

        if Usuario.objects.filter(email=correo).exists():

            messages.error(
                request,
                "El correo ya está registrado."
            )

            return redirect('register')

        user = Usuario.objects.create_user(
            username=usuario,
            email=correo,
            password=clave,
            nombres=nombres,
            apellidos=apellidos
        )

        auth_login(request, user)

        messages.success(
            request,
            "Cuenta creada correctamente."
        )

        return redirect('dashboard')

    return render(request, 'registro.html')


@login_required
def dashboard(request):

    eventos = Evento.objects.filter(
        id_creador=request.user
    )

    foros = Foro.objects.filter(
        id_creador=request.user
    )

    total_asistentes = sum(
        evento.asistentes.count()
        for evento in eventos
    )

    context = {

        'eventos': eventos,
        'foros': foros,

        'total_eventos': eventos.count(),
        'total_foros': foros.count(),
        'total_asistentes': total_asistentes

    }

    return render(
        request,
        'dashboardUser.html',
        context
    )