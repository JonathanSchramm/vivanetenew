from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_planos, name='lista_planos'),
]
