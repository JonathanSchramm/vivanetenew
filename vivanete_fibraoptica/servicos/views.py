from django.shortcuts import render
from .models import Plano

def lista_planos(request):
    planos = Plano.objects.all()
    return render(request, 'servicos/lista_planos.html', {'planos': planos})
