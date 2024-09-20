from django.shortcuts import render, redirect
from .models import Cliente
from .forms import ClienteForm
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})

@login_required
def adicionar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/adicionar_cliente.html', {'form': form})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro realizado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = RegistroForm()
    return render(request, 'clientes/registro.html', {'form': form})