from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Evento
from .forms import EventoForm


def event_list_view(request):
    eventos = Evento.objects.all().order_by('-f_inicio') 
    query_busqueda = request.GET.get('q')
    
    if query_busqueda:
        eventos = eventos.filter(titulo__icontains=query_busqueda)
        
    return render(request, 'event/event_list.html', {
        'eventos': eventos,
        'now': timezone.now()
    })

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.id_creador = request.user
            evento.save()
            return redirect('event_list') 
    else:
        form = EventoForm()
    return render(request, 'event/formsEvent.html', {'form': form, 'accion': 'Crear'})

@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, id_creador=request.user)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=evento.pk) 
    else:
        form = EventoForm(instance=evento)
    return render(request, 'event/formsEvent.html', {'form': form, 'evento': evento, 'accion': 'Editar'})

@login_required
def unirse_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.user in evento.asistentes.all():
        evento.asistentes.remove(request.user)
    else:
        evento.asistentes.add(request.user)
    return redirect('event_detail', pk=evento.pk)

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
    return render(request, 'event/event_detail.html', {
        'evento': evento,
        'now': timezone.now()
    })