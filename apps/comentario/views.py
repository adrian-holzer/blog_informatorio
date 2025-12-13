# apps/comentario/views.py
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Comentario
from .forms import ComentarioForm 

from apps.articulo.models import Articulo 
def is_colaborador(user):
    
    if user.is_superuser:
        return True
    return False 

@login_required
def editarComentario(request, pk_comentario):
    comentario = get_object_or_404(Comentario, pk=pk_comentario)
    user = request.user
    
  
    es_dueno = (comentario.usuario == user)
    es_colab_o_super = is_colaborador(user) or user.is_superuser
    
    if not (es_dueno or es_colab_o_super):
        return HttpResponseForbidden("No tienes permiso para editar este comentario.")
        
    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, "Comentario actualizado exitosamente.")
            # Redirigir al detalle del artículo
            return redirect('apps.articulo:detalle_articulo', pk=comentario.articulo.pk)
    else:
        form = ComentarioForm(instance=comentario)
        
    contexto = {
        'form': form,
        'comentario': comentario,
        'articulo': comentario.articulo
    }
    
    return render(request, 'comentario/agregarComentario.html', contexto)


# ----------------------------------------------------
# 3. ELIMINACIÓN DE COMENTARIO
# ----------------------------------------------------

@login_required
def eliminarComentario(request, pk_comentario):
    comentario = get_object_or_404(Comentario, pk=pk_comentario)
    user = request.user
    
   
    es_dueno = (comentario.usuario == user)
    es_colab_o_super = is_colaborador(user) or user.is_superuser
    
    if not (es_dueno or es_colab_o_super):
        return HttpResponseForbidden("No tienes permiso para eliminar este comentario.")
        
    if request.method == 'POST':
        comentario.delete()
        messages.success(request, "Comentario eliminado exitosamente.")
        
        return redirect('apps.articulo:detalle_articulo', pk=comentario.articulo.pk)
        
    contexto = {
        'comentario': comentario,
        'mensaje': f"Eliminando comentario de {comentario.usuario.username}",
    }
    return render(request, 'comentario/eliminarComentario.html', contexto)