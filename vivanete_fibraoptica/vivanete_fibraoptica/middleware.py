from django.http import HttpResponseNotFound
from django.conf import settings

class AdminIPRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_ips = getattr(settings, 'AUTHORIZED_IPS', [])

    def __call__(self, request):
        ip = self.get_client_ip(request)
        if request.path.startswith('/admin/') and ip not in self.allowed_ips:
            # return HttpResponseForbidden("Acesso negado.")
            return HttpResponseNotFound('<h1>Página Não Encontrada</h1><p>O objeto solicitado não existe.</p>')
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        # Verifica se o IP está nos cabeçalhos HTTP_X_FORWARDED_FOR (em caso de proxies)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Pode haver uma lista de IPs no cabeçalho, pega o primeiro
            ip = x_forwarded_for.split(',')[0]
        else:
            # Caso contrário, usa REMOTE_ADDR
            ip = request.META.get('REMOTE_ADDR')
        return ip
