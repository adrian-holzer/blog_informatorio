from django.urls import path
from . import views 

app_name =  'apps.articulo'

urlpatterns = [
   
    path('articulos', views.lista_articulos, name='lista_articulos'),
    
   
    path('crear/', views.crear_articulo, name='crear_articulo'),
    
    path('articulo/<int:pk>/', views.detalle_articulo, name='detalle_articulo'),
    
    path('<int:pk>/editar/', views.editar_articulo, name='editar_articulo'),
    
    path('<int:pk>/eliminar/', views.eliminar_articulo, name='eliminar_articulo'),
    
]