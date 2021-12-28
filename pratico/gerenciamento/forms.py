from django import forms
from django.forms.widgets import Textarea

from .models import LocalPraticaEsportiva


class LocalPraticaEsportivaForm(forms.ModelForm):
    class Meta:
        model = LocalPraticaEsportiva
        exclude = ['longitude', 'latitude', 'postador']
        widgets = {'descricao': Textarea(attrs={'rows': 4, 'cols': 15})}
