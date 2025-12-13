from django.views.generic import TemplateView
from apps.articulo.models import Articulo, Categoria


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Último artículo publicado y activo
        context['ultimo_articulo'] = (
            Articulo.objects
            .filter(activo=True)
            .order_by('-fecha_publicacion')
            .first()
        )

        # Todas las categorías reales
        context['categorias'] = Categoria.objects.all()

        return context


class AcercaView(TemplateView):
    template_name = 'acerca.html'
