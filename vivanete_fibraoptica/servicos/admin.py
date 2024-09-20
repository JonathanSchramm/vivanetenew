from django.contrib import admin
from .models import Plano

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'velocidade', 'preco', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'velocidade')