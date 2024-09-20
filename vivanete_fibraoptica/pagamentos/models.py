from django.db import models
from clientes.models import Cliente
from servicos.models import Plano

class Pagamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, default='Pendente')
    txid = models.CharField(max_length=35, blank=True, null=True)
    qr_code = models.TextField(blank=True, null=True)
    qr_code_imagem = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.cliente.nome} - {self.plano.nome}"
