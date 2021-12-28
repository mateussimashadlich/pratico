from django import forms
from django.contrib.auth.forms import UserCreationForm


class UsuarioForm(UserCreationForm):
    error_messages = {
        'password_mismatch': ("As senhas não coincidem."),
    }
    password1 = forms.CharField(label=("Senha"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Confirmação da senha"),
                                widget=forms.PasswordInput,
                                help_text=("Insira a mesma senha de cima para verificação."))

    class Meta(UserCreationForm.Meta):
        labels = {
            'username': 'Usuário',
        }
