from django.db import models

class Plano(models.Model):
    nome = models.CharField(max_length=100)
    velocidade = models.CharField(max_length=50)  # Exemplo: "100 Mbps"
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {self.velocidade}"
