from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# models

class Usuario(AbstractUser):
   
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios_personalizados',
       
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='permisos_usuarios_personalizados', 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    imagen = models.ImageField(null=True, blank=True, upload_to='usuario', default='usuario/user_default.jpg')

    def get_absolute_url(self):
        return reverse('index')

