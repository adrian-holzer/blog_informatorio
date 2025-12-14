from django.views.generic import ListView, TemplateView # Se añade ListView
from apps.articulo.models import Articulo, Categoria


class IndexView(ListView): # La vista de inicio ahora es una ListView
    model = Articulo # Indica a la vista que debe buscar objetos del modelo Articulo
    template_name = 'index.html'
    context_object_name = 'object_list' # Esto garantiza que la lista se envíe a index.html como 'object_list'

    def get_queryset(self):
        # Esta función obtiene solo los artículos activos, ordenados del más nuevo al más viejo (últimos 6)
        # Esto reemplaza la lógica de 'get_context_data' que solo traía uno.
        return Articulo.objects.filter(activo=True).order_by('-fecha_publicacion')[:6] 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Todas las categorías reales (Se mantiene para el sidebar)
        context['categorias'] = Categoria.objects.all()

        return context


class AcercaView(TemplateView):
    template_name = 'acerca.html'