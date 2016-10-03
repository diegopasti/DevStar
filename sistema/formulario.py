# -*- encoding: utf-8 -*-
from django import forms

MENSAGENS_ERROS={'required': 'Precisa ser Informado!',
                 'invalid' : 'Formato Inválido!'
                }


class formulario_login(forms.Form):

    usuario = forms.CharField(label="Usuario:", max_length=100, required=True, error_messages=MENSAGENS_ERROS,
                               widget=forms.TextInput(attrs={'class': "form-control", 'id': 'usuario','readonly':True,'type':"hidden" }), )

    senha = forms.CharField(label="Senha:", max_length=50, required=True, error_messages=MENSAGENS_ERROS,
                                 widget=forms.TextInput(attrs={'class': "form-control", 'id': 'senha','readonly':True,'type':"hidden" }), )

class formulario_register(forms.Form):

    usuario = forms.CharField(label="Usuario:", max_length=100, required=True, error_messages=MENSAGENS_ERROS,
                               widget=forms.TextInput(attrs={'class': "form-control", 'id': 'usuario','readonly':True,'type':"hidden" }), )

    senha = forms.CharField(label="Senha:", max_length=50, required=True, error_messages=MENSAGENS_ERROS,
                                 widget=forms.TextInput(attrs={'class': "form-control", 'id': 'senha','readonly':True,'type':"hidden" }), )

    confirme_senha = forms.CharField(label="Confirme a Senha:", max_length=50, required=True, error_messages=MENSAGENS_ERROS,
                            widget=forms.TextInput(
                                attrs={'class': "form-control", 'id': 'confirme_senha', 'readonly': True,'type':"hidden" }), )