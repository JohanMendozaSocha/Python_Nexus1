from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evento
from .forms import EventoForm


def event_list_view(request):
    eventos = Evento.objects.all().order_by('-f_inicio') 
    return render(request, 'event/event_list.html', {'eventos': eventos})

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.id_creador = request.user
            evento.save()
            return redirect('event_list') 
    else:
        form = EventoForm()
    return render(request, 'event/formsEvent.html', {'form': form})

@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, id_creador=request.user)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('event_list') 
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
    return redirect('event_list')

@login_required
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, id_creador=request.user)
    evento.delete()
    return redirect('event_list') 

@login_required
def reportar_evento(request, pk):
    return redirect('event_list') 

def event_detail_view(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'event/event_detail.html', {'evento': evento})