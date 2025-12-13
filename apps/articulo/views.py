# articulo/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Articulo, Categoria
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


def lista_articulos(request):
    
    articulos = Articulo.objects.filter(activo=True)
  
    filtro_categoria = request.GET.get('categoria', None) 
    orden_por = request.GET.get('orden', 'fecha_desc') 
    if filtro_categoria:
        try:
            articulos = articulos.filter(categoria__pk=int(filtro_categoria))
        except ValueError:
            pass 
            
    if orden_por == 'fecha_asc':
        articulos = articulos.order_by('fecha_publicacion')
    elif orden_por == 'fecha_desc':
        articulos = articulos.order_by('-fecha_publicacion') 
    elif orden_por == 'titulo_asc':
        articulos = articulos.order_by('titulo') 
    elif orden_por == 'titulo_desc':
        articulos = articulos.order_by('-titulo') 
    
    todas_las_categorias = Categoria.objects.all()
    
    articulos_data = []
    for articulo in articulos:
        can_edit = False
        if request.user.is_authenticated:
            is_owner = (articulo.editor == request.user)
            is_superuser_or_colab = request.user.is_superuser 
            can_edit = is_owner or is_superuser_or_colab

        articulos_data.append({
            'articulo': articulo,
            'can_edit': can_edit,
        })
        
    contexto = {
        'articulos_data': articulos_data,
        'categorias': todas_las_categorias,
        'filtro_categoria_actual': filtro_categoria, 
        'orden_actual': orden_por,
    }
    
    return render(request, 'articulo/lista_articulos.html', contexto)

def detalle_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk, activo=True)
    user = request.user
    
    comentario_form = None
    if user.is_authenticated:
        if request.method == 'POST':
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                nuevo_comentario = comentario_form.save(commit=False)
                nuevo_comentario.articulo = articulo
                nuevo_comentario.usuario = user
                nuevo_comentario.save()
                messages.success(request, "Tu comentario ha sido publicado.")
                return redirect('apps.articulo:detalle_articulo', pk=articulo.pk)
        else:
            comentario_form = ComentarioForm()
    
    comentarios = articulo.comentarios.all().order_by('fecha')
    
    comentarios_data = []
    is_colab_or_super = es_colaborador(user) or user.is_superuser
    
    for comentario in comentarios:
        can_edit_or_delete = False
        
        if user.is_authenticated:
            es_dueno = (comentario.usuario == user)
            
            if es_dueno or is_colab_or_super:
                can_edit_or_delete = True
        
        comentarios_data.append({
            'comentario': comentario,
            'can_manage': can_edit_or_delete 
        })

    contexto = {
        'articulo': articulo,
        'comentario_form': comentario_form,
        'comentarios_data': comentarios_data,
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