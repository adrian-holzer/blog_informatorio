# articulo/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Articulo
from .forms import ArticuloForm
from django.contrib.auth.models import Group 
from apps.comentario.forms import ComentarioForm 
def es_colaborador(user):
    if not user.is_authenticated:
        return False
    try:
        colaborador_group = Group.objects.get(name='Colaborador')
        return colaborador_group in user.groups.all()
    except Group.DoesNotExist:
        return False

# Lista de articulos activos 

def lista_articulos(request):
    articulos_qs = Articulo.objects.filter(activo=True)
    articulos_data = []
    user = request.user
    
    # Pre-calcular el permiso de Colaborador (solo una vez)
    is_colab = es_colaborador(user)
    is_super = user.is_superuser
    
    for articulo in articulos_qs:
        # Lógica de Permisos: ¿Puede el usuario actual editar/eliminar este artículo?
        # Requisito: Es dueño O es colaborador O es superusuario
        can_edit = False
        if user.is_authenticated:
            es_dueno = (articulo.editor == user)
            
            if es_dueno or is_colab or is_super:
                can_edit = True
        
        # Crear un diccionario que combina el objeto Articulo con el permiso calculado
        articulos_data.append({
            'articulo': articulo,
            'can_edit': can_edit
        })
        
    contexto = {'articulos_data': articulos_data} # Cambiamos el nombre de la variable de contexto
    return render(request, 'articulo/lista_articulos.html', contexto)

#  Muestra un artículo específico.

def detalle_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk, activo=True)
    user = request.user
    
    # Lógica de permisos para la edición del ARTÍCULO (que ya teníamos)
    can_edit_articulo = False
    if user.is_authenticated:
        es_dueno = (articulo.editor == user)
        es_colab = es_colaborador(user)
        if es_dueno or es_colab or user.is_superuser:
            can_edit_articulo = True

    # 1. Manejo de la CREACIÓN de Comentarios (Si el usuario está logueado y envió un POST)
    if request.method == 'POST' and user.is_authenticated:
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            nuevo_comentario = comentario_form.save(commit=False)
            nuevo_comentario.articulo = articulo
            nuevo_comentario.usuario = user
            nuevo_comentario.save()
            messages.success(request, "Tu comentario ha sido publicado.")
            # Redirigir a la misma página para evitar reenvío del formulario (patrón PRG)
            return redirect('apps.articulo:detalle_articulo', pk=articulo.pk)
    else:
        # El formulario se crea vacío para mostrarlo si el usuario está logueado
        comentario_form = ComentarioForm()
        
    
    # 2. LISTADO DE COMENTARIOS (READ)
    # Se obtienen todos los comentarios activos del artículo
    comentarios = articulo.comentarios.all().order_by('-fecha')
    
    # Preparamos los datos para el template, incluyendo el permiso de edición/eliminación
    comentarios_data = []
    is_colab = es_colaborador(user)
    is_super = user.is_superuser
    
    for comentario in comentarios:
        can_edit_comentario = False
        
        # El usuario logueado puede editar/eliminar un comentario si:
        if user.is_authenticated:
            es_dueno = (comentario.usuario == user)
            
            # Es dueño O (Es Colaborador O Superuser)
            if es_dueno or is_colab or is_super:
                can_edit_comentario = True
        
        comentarios_data.append({
            'comentario': comentario,
            'can_edit': can_edit_comentario
        })

    contexto = {
        'articulo': articulo,
        'comentario_form': comentario_form,
        'comentarios_data': comentarios_data,
        'can_edit_articulo': can_edit_articulo,
    }
    return render(request, 'articulo/detalle_articulo.html', contexto)
# ----------------------------------------------------
 # CREAR
# ----------------------------------------------------

@login_required
def crear_articulo(request):

    if request.method == 'POST':
        
        form = ArticuloForm(request.POST, request.FILES) 
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.editor = request.user
            articulo.save()
            return redirect('apps.articulo:lista_articulos')
    else:
        form = ArticuloForm()
        
    contexto = {'form': form, 'accion': 'Crear'}
    return render(request, 'articulo/crear_articulo.html', contexto)


# ----------------------------------------------------
#   ACTUALIZAR
# ----------------------------------------------------

@login_required
def editar_articulo(request, pk):

    articulo = get_object_or_404(Articulo, pk=pk)
    
    # Control de Permisos

    if articulo.editor != request.user and not request.user.is_superuser:
        raise PermissionDenied("No tienes permiso para editar este artículo.")
        
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('apps.articulo:lista_articulos')
    else:
        form = ArticuloForm(instance=articulo)
        
    contexto = {'form': form, 'articulo': articulo, 'accion': 'Editar'}
    return render(request, 'articulo/crear_articulo.html', contexto)


# ----------------------------------------------------
# BORRAR
# ----------------------------------------------------

@login_required
def eliminar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)

    # Control de Permisos
    if articulo.editor != request.user and not request.user.is_superuser:
        raise PermissionDenied("No tienes permiso para eliminar este artículo.")
        
    if request.method == 'POST':
        articulo.delete()
        return redirect('apps.articulo:lista_articulos') 
        
    contexto = {'articulo': articulo}
    return render(request, 'articulo/eliminar_articulo.html', contexto)