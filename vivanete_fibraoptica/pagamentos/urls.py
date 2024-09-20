from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pagamentos, name='lista_pagamentos'),
    path('realizar/', views.realizar_pagamento, name='realizar_pagamento'),
    path('detalhe/<int:pagamento_id>/', views.detalhe_pagamento, name='detalhe_pagamento'),
    path('webhook/', views.webhook_pix, name='webhook_pix'),
]
