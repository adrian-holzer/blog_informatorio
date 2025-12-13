from django.urls import path
from . import views 


app_name = 'apps.comentario'

urlpatterns = [
    path('comentario/<int:pk_comentario>/editar/', views.editarComentario, name='editarComentario'),
    path('comentario/<int:pk_comentario>/eliminar/', views.eliminarComentario, name='eliminarComentario'),
]