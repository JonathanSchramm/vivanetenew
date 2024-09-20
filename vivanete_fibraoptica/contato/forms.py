# forms.py
from django import forms
from django_recaptcha.fields import ReCaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu nome completo',
            'id': 'id_name'
        }),
        label='Nome'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu email',
            'id': 'id_email'
        }),
        label='Email'
    )
    subject = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Assunto',
            'id': 'id_subject'
        }),
        label='Assunto'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Escreva sua mensagem aqui...',
            'rows': 5,
            'id': 'id_message'
        }),
        label='Mensagem'
    )
    captcha = ReCaptchaField()
