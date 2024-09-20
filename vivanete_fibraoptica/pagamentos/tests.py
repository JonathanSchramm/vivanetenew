from django.test import TestCase
from django.urls import reverse
from .models import Pagamento
from clientes.models import Cliente
from servicos.models import Plano

class PagamentoTestCase(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome='Teste Cliente',
            email='cliente@teste.com',
            endereco='Rua Teste, 123',
            telefone='123456789'
        )
        self.plano = Plano.objects.create(
            nome='Plano Teste',
            velocidade='100Mbps',
            preco=99.99,
            descricao='Plano de teste'
        )

    def test_realizar_pagamento(self):
        self.client.login(username='cliente', password='senha123')
        response = self.client.post(reverse('realizar_pagamento'), {
            'cliente': self.cliente.id,
            'plano': self.plano.id,
            'valor': 99.99
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Pagamento.objects.count(), 1)
