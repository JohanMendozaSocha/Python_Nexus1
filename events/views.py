from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evento
from .forms import EventoForm

def panel_eventos(request):
    usuario_actual = request.user if request.user.is_authenticated else None
    ver_mis_eventos = request.GET.get('mis_eventos') == 'true'
    
    if ver_mis_eventos and usuario_actual:
        eventos = Evento.objects.filter(id_creador=usuario_actual).order_by('-created_at')
    else:
        eventos = Evento.objects.all().order_by('-created_at')

    buscar = request.GET.get('buscar')
    if buscar:
        eventos = eventos.filter(titulo__icontains=buscar)

    context = {
        'eventos': eventos,
        'buscar': buscar if buscar else '',
        'ver_mis_eventos': ver_mis_eventos
    }
    return render(request, 'event/createEvent.html', context)

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.id_creador = request.user
            evento.save()
            return redirect('panel_eventos')
    else:
        form = EventoForm()
    
    return render(request, 'event/formsEvent.html', {'form': form})

@login_required
def editar_evento(request, pk):
    # 🌟 CORREGIDO: Se agregó el ', pk' arriba para que Django sepa qué evento editar
    evento = get_object_or_404(Evento, pk=pk, id_creador=request.user)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('panel_eventos')
    else:
        form = EventoForm(instance=evento)
        
    return render(request, 'event/formsEvent.html', {'form': form})

@login_required
def unirse_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.user in evento.asistentes.all():
        evento.asistentes.remove(request.user)
    else:
        evento.asistentes.add(request.user)
    return redirect('panel_eventos')

@login_required
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, id_creador=request.user)
    evento.delete()
    return redirect('panel_eventos')

@login_required
def reportar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    print(f"El usuario {request.user.username} reportó el evento {evento.titulo}")
    return redirect('panel_eventos')