from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
# 👈 IMPORTANTE: Importamos tu propio modelo personalizado de usuario
from .models import Usuario 

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')

        user = authenticate(request, username=usuario, password=clave)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f"¡Autenticación exitosa! Bienvenido, {user.username}.")
            return redirect('login')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return redirect('login')

    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        correo = request.POST.get('email')
        clave = request.POST.get('password')
        confirmar_clave = request.POST.get('confirm_password')

        # 1. Validar contraseñas
        if clave != confirmar_clave:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')

        # 2. Validar que el usuario no exista (Usando tu modelo Usuario)
        if Usuario.objects.filter(username=usuario).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('register')

        # 3. Validar que el correo no esté registrado
        if Usuario.objects.filter(email=correo).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return redirect('register')

        # 4. Crear el usuario usando la función correcta de Django
        user = Usuario.objects.create_user(username=usuario, email=correo, password=clave)
        user.save()

        # 5. Autenticar e Iniciar sesión automáticamente
        auth_login(request, user)
        messages.success(request, "¡Cuenta creada con éxito! Ya estás registrado.")
        return redirect('login')

    return render(request, 'registro.html')