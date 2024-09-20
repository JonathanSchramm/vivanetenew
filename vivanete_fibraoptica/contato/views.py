# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import datetime

def contato(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extrair dados do formulário
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Preparar o contexto para o template de email
            context = {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
                'current_year': datetime.now().year,
            }

            # Renderizar o template de email HTML
            html_content = render_to_string('contato/envio_email.html', context)
            # Gerar o texto puro do email a partir do HTML
            text_content = strip_tags(html_content)

            # Configurar o email
            email_message = EmailMultiAlternatives(
                subject=f"Contato: {subject}",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],  # Email de destino definido nas configurações
                reply_to=[email],  # Permite responder diretamente ao remetente
            )
            email_message.attach_alternative(html_content, "text/html")

            try:
                # Enviar o email
                email_message.send()
                messages.success(request, 'Sua mensagem foi enviada com sucesso!')
                return redirect('contato')
            except Exception as e:
                print(f"Erro ao enviar email: {e}")
                messages.error(request, 'Ocorreu um erro ao enviar sua mensagem. Por favor, tente novamente mais tarde.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = ContactForm()

    return render(request, 'contato/contato.html', {'form': form})
