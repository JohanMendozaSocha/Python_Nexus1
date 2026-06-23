from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evento
from .forms import EventoForm

# 1. VISTA PRINCIPAL: LISTAR, BUSCAR Y MOSTRAR EL MODAL DE CREAR
def panel_eventos(request):
    # Aquí asumimos temporalmente un usuario para que no se estalle si no hay login hecho
    # Cuando tengas el login listo, cambias esto por: usuario_actual = request.user
    usuario_actual = request.user if request.user.is_authenticated else None

    # Traer solo los eventos creados por este usuario
    eventos = Evento.objects.filter(id_creador=usuario_actual) if usuario_actual else Evento.objects.all()

    # Lógica de la barra de búsqueda (si el usuario escribe algo en el input)
    buscar = request.GET.get('buscar')
    if buscar:
        eventos = eventos.filter(nombre__icontains=buscar) # Filtra por nombre sin importar mayúsculas

    # Lógica para procesar el formulario de CREAR (el que va dentro del modal)
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            if usuario_actual:
                evento.id_creador = usuario_actual
            evento.save()
            return redirect('panel_eventos')
    else:
        form = EventoForm()

    context = {
        'eventos': eventos,
        'form': form,
        'buscar': buscar if buscar else ''
    }
    return render(request, 'event/createEvent.html', context)


# 2. VISTA PARA ACTUALIZAR (EDITAR) UN EVENTO
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('panel_eventos')
    return redirect('panel_eventos')


# 3. VISTA PARA ELIMINAR (BORRAR) UN EVENTO
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        evento.delete()
    return redirect('panel_eventos')