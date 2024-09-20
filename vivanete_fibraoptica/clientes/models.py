from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15)
    cpf = models.CharField(default='000.000.000-00',max_length=14, unique=True)  # Novo campo

    def __str__(self):
        return self.nome

