from .forms import ContactoForm
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect

class ContactoUsuario(CreateView):
    template_name = 'contacto/contacto.html'
    form_class = ContactoForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
       self.object = form.save()

       url_exitosa = reverse('apps.contacto:contacto') + '?enviado=true'
        
       return redirect(url_exitosa)