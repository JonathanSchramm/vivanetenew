from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL personalizada do admin
    path('painel-adm/', admin.site.urls),

    # Sua página inicial
    path('', views.home, name='home'),
    
    path('servicos/', include('servicos.urls')),

    path('sobre/', include('sobre.urls')),

    path('contato/', include('contato.urls')),
    # Inclua as URLs de autenticação padrão do Django
    # path('accounts/', include('django.contrib.auth.urls')),

    # Inclua as URLs do two_factor dentro de 'accounts/'
    # path('', include('two_factor.urls')),
    # Outras rotas
    # path('clientes/', include('clientes.urls')),
    # path('pagamentos/', include('pagamentos.urls')),
    # path('login/', auth_views.LoginView.as_view(template_name='clientes/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Adiciona a configuração para servir arquivos de mídia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
