from django import forms
from .models import Cliente
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if not telefone.isdigit():
            raise forms.ValidationError("O telefone deve conter apenas números.")
        return telefone

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
