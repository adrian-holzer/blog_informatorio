from django.contrib import admin
from django.urls import path, include
from .views import IndexView, AcercaView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexView.as_view(), name='index'),
    path('acerca/', AcercaView.as_view(), name='acerca'),

    path('', include('apps.articulo.urls')),
    path('', include('apps.contacto.urls')),
    path('', include('apps.usuario.urls')),
    path('', include('apps.comentario.urls')),

    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
