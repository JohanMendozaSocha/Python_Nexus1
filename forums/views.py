from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Foro, Publicacion, Reporte
from django.db.models import Count

# 1. VER TODOS LOS FOROS

def lista_foros(request):

    foros = Foro.objects.annotate(num_respuestas=Count('publicacion')).order_by('-created_at')
    query = request.GET.get('search', '')
    
    if query:
        
        foros = Foro.objects.filter(titulo__icontains=query).order_by('-created_at')
    else:
        
        foros = Foro.objects.all().order_by('-created_at')
        
    return render(request, 'forums/forum_list.html', {
        'foros': foros,
        'query': query  
    })

# 2. VER UN FORO Y SUS COMENTARIOS 
def detalle_foro(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)
    
    if request.method == 'POST':
        # Detectar si es una petición AJAX (JS) o normal
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        
        contenido = request.POST.get('contenido')
        if contenido:
            nueva_pub = Publicacion.objects.create(
                contenido=contenido,
                id_foro=foro,
                id_usuario=request.user
            )
            
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'username': request.user.username,
                    'contenido': nueva_pub.contenido
                })
            return redirect('forum_detail', foro_id=foro.id)

    publicaciones = Publicacion.objects.filter(id_foro=foro).order_by('created_at')
    return render(request, 'forums/forum_detail.html', {
        'foro': foro,
        'publicaciones': publicaciones
    })
 

# 3. CREAR UN FORO 
@login_required
def crear_foro(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        categoria = request.POST.get('categoria')
        
        if titulo and descripcion:
            Foro.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                categoria=categoria,
                id_creador=request.user
            )
            return redirect('forum_list') 
            
    return render(request, 'forums/forum_create.html')

#  ELIMINAR UN FORO 
@login_required
def eliminar_foro(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)
  
    if foro.id_creador == request.user:
        foro.delete()
        
    return redirect('forum_list')

#  ELIMINAR UN COMENTARIO/PUBLICACIÓN 
@login_required
def eliminar_publicacion(request, pub_id):
    publicacion = get_object_or_404(Publicacion, id=pub_id)
    foro_id = publicacion.id_foro.id 
    
   
    if publicacion.id_usuario == request.user:
        publicacion.delete()
        
    return redirect('forum_detail', foro_id=foro_id)

# 6. REPORTAR UN FORO O UNA PUBLICACIÓN
@login_required
def reportar_contenido(request):
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        comentario = request.POST.get('comentario', '')
        foro_id = request.POST.get('foro_id')
        pub_id = request.POST.get('pub_id')
        
        nuevo_reporte = Reporte(
            motivo=motivo,
            comentario_adicional=comentario,
            id_usuario=request.user
        )
        
        if foro_id:
            nuevo_reporte.id_foro = get_object_or_404(Foro, id=foro_id)
            nuevo_reporte.save()
            return redirect('forum_list')
            
        if pub_id:
            publicacion = get_object_or_404(Publicacion, id=pub_id)
            nuevo_reporte.id_publicacion = publicacion
            nuevo_reporte.save()
            return redirect('forum_detail', foro_id=publicacion.id_foro.id)
            
    return redirect('forum_list')
# 7. VISTA PERSONALIZADA PARA ERROR 404
def error_404_view(request, exception):
    return render(request, '404.html', status=404)

# forums/views.py

def forum_list_view(request):
    """Vista para explorar todos los foros"""
    foros = Foro.objects.all()
    query = request.GET.get('search', '')
    if query:
        foros = foros.filter(titulo__icontains=query)
    
    return render(request, 'forums/forum_list.html', {'foros': foros, 'query': query})

def mis_foros_view(request):
    """Vista exclusiva para ver mis foros"""
    
    foros = Foro.objects.filter(id_creador=request.user)
    query = request.GET.get('search', '')
    if query:
        foros = foros.filter(titulo__icontains=query)
        
    return render(request, 'forums/forum_me.html', {'foros': foros, 'query': query})