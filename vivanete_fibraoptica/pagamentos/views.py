from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pagamento
from .forms import PagamentoForm
from django.conf import settings
from clientes.models import Cliente
from servicos.models import Plano
from gerencianet import Gerencianet
import uuid
import base64
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string

@login_required
def realizar_pagamento(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            cliente = pagamento.cliente
            plano = pagamento.plano
            valor = float(pagamento.valor)
            valor_formatado = f"{valor:.2f}"

            # Configuração da API Gerencianet
            gn_credentials = {
                'client_id': settings.GERENCIANET_CLIENT_ID,
                'client_secret': settings.GERENCIANET_CLIENT_SECRET,
                'sandbox': settings.GERENCIANET_AMBIENTE == 'sandbox',
                'certificate': settings.GERENCIANET_CERTIFICADO
            }

            gn = Gerencianet(gn_credentials)

            # Gerar um txid único (máximo 35 caracteres)
            txid = uuid.uuid4().hex[:26]  # Ajuste para não exceder o limite

            # Dados da cobrança
            body = {
                "calendario": {
                    "expiracao": 3600
                },
                "devedor": {
                    "cpf": cliente.cpf,
                    "nome": cliente.nome
                },
                "valor": {
                    "original": valor_formatado
                },
                "chave": settings.GERENCIANET_CHAVE_PIX,
                "solicitacaoPagador": f"Pagamento do plano {plano.nome}"
            }

            try:
                # Cria a cobrança
                response_cobranca = gn.pix_create_charge(txid, body)
                # Gera o QR Code
                response_qrcode = gn.pix_generate_QRCode(txid)
                pagamento.status = 'Aguardando'
                pagamento.txid = txid
                pagamento.qr_code = response_qrcode['qrcode']
                pagamento.qr_code_imagem = response_qrcode['imagemQrcode']
                pagamento.save()
                return redirect('detalhe_pagamento', pagamento_id=pagamento.id)
            except Exception as e:
                # Trate erros de acordo
                erro = e.args[0]
                return render(request, 'pagamentos/erro_pagamento.html', {'erro': erro})
    else:
        form = PagamentoForm()
    return render(request, 'pagamentos/realizar_pagamento.html', {'form': form})

@login_required
def atualizar_status_pagamento(pagamento):
    gn_credentials = {
        'client_id': settings.GERENCIANET_CLIENT_ID,
        'client_secret': settings.GERENCIANET_CLIENT_SECRET,
        'sandbox': settings.GERENCIANET_AMBIENTE == 'sandbox',
        'certificate': settings.GERENCIANET_CERTIFICADO
    }

    gn = Gerencianet(gn_credentials)
    try:
        response = gn.pix_detail_charge(pagamento.txid)
        status = response.get('status')
        if status == 'CONCLUIDA' and pagamento.status != 'Pago':
            pagamento.status = 'Pago'
            pagamento.save()
            # Enviar email de confirmação
            assunto = 'Pagamento Confirmado'
            mensagem = render_to_string('pagamentos/email_confirmacao.html', {'pagamento': pagamento})
            destinatario = [pagamento.cliente.email]
            send_mail(assunto, mensagem, settings.DEFAULT_FROM_EMAIL, destinatario)
    except Exception as e:
        pass  

@login_required
def detalhe_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    atualizar_status_pagamento(pagamento)
    return render(request, 'pagamentos/detalhe_pagamento.html', {'pagamento': pagamento})

@login_required
def lista_pagamentos(request):
    pagamentos = Pagamento.objects.all()
    return render(request, 'pagamentos/lista_pagamentos.html', {'pagamentos': pagamentos})

@csrf_exempt 
def webhook_pix(request):
    if request.method == 'POST':
        notificacao = json.loads(request.body.decode('utf-8'))
        txid = notificacao['pix'][0]['txid']

        # Atualize o status do pagamento
        pagamento = Pagamento.objects.get(txid=txid)
        pagamento.status = 'Pago'
        pagamento.save()

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)