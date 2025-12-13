from .models import Usuario
from .forms import RegistroUsuarioForm
from ..articulo.models import Articulo
from ..comentario.models import Comentario
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.generic import CreateView, ListView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View


class RegistrarUsuario(CreateView):
    template_name = 'registration/registrar.html'
    form_class = RegistroUsuarioForm

    def form_valid(self, form):
        response = super().form_valid(form)
      
        messages.success(self.request, 'Registro exitoso. Por favor, inicia sesión.')
        group, created = Group.objects.get_or_create(name='Miembro')
        self.object.groups.add(group)
        return redirect('apps.usuario:login')

class LoginUsuario(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        messages.success(self.request, 'Login exitoso')
        return reverse('index')
     
class LogoutUsuario(LogoutView):
    template_name = 'registration/logout.html'

    def dispatch(self, request, *args, **kwargs):
        
    
        super().dispatch(request, *args, **kwargs) 
        
        messages.success(request, 'Cierre de sesión exitoso.')
      
        return redirect(reverse('index'))
    
    
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuario/usuario_list.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(is_superuser=True)
        return queryset

class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    success_url = reverse_lazy('apps.usuario:usuario_list')
    template_name = 'usuario/eliminar_usuario.html'  # se mantiene por compatibilidad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            colaborador_group = Group.objects.get(name='Colaborador')
            context['es_colaborador'] = colaborador_group in self.object.groups.all()
        except Group.DoesNotExist:
            context['es_colaborador'] = False
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Seguridad: no permitir eliminar superusuarios
        if self.object.is_superuser:
            messages.error(request, "No se puede eliminar un administrador.")
            return redirect(self.success_url)

        eliminar_comentarios = request.POST.get('eliminar_comentarios')
        eliminar_posts = request.POST.get('eliminar_posts')

        if eliminar_comentarios:
            Comentario.objects.filter(usuario=self.object).delete()

        if eliminar_posts:
            Articulo.objects.filter(autor=self.object).delete()

        username = self.object.username
        self.object.delete()

        messages.success(request, f'Usuario {username} eliminado correctamente.')
        return redirect(self.success_url)
    
    
class MyPasswordResetView(PasswordResetView):
    template_name = 'registration/recuperar_contraseña.html'

    def get_success_url(self):
        messages.success(self.request, 'Se envió un email de recuperación. Revise su casilla de correo para recuperar su cuenta.')
        return reverse('index')

class UsuarioUpdateGroupView(View):
    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        grupo_nombre = request.POST.get('grupo')

        usuario.groups.clear()

        if grupo_nombre:
            grupo, _ = Group.objects.get_or_create(name=grupo_nombre)
            usuario.groups.add(grupo)

        messages.success(
            request,
            f'Grupo del usuario {usuario.username} actualizado a {grupo_nombre}'
        )
        return redirect('apps.usuario:usuario_list')
