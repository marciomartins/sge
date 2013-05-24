# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from django.forms import ModelForm, ModelChoiceField, Textarea, TextInput, DateInput, HiddenInput
from django.forms.models import inlineformset_factory

from sge.source import choices
from sge.source.models import *

__all__ = ('UserForm', 'ClienteForm', 'ProdutoForm', 'ClienteProdutoFormSet', 'LocomocaoForm', 
           'EntregadorForm', 'EntregadorClienteForm', 'EntregadorClienteFormSet',
           'EntregaForm', 'EntregaClienteForm', 'EntregaClienteFormSet', 
           'EntregaFormConsulta', 'EntregaClienteFormConsulta', 'EntregaClienteFormSetConsulta', 
           'TransferenciaForm', 'TransferenciaClienteForm', 'TransferenciaClienteFormSet',
           'TransferenciaFormConsulta', 'TransferenciaClienteFormConsulta', 'TransferenciaClienteFormSetConsulta')
           
class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ('password' ,'is_staff','is_active', 'is_superuser', 'groups', 'user_permissions', 'last_login','date_joined')
        widgets = {}

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        widgets = {
            'obs': Textarea(attrs={'rows': 5}),
            'cnpj': TextInput(attrs={'class': 'input-medium mask-cnpj'}),
            'razao_social': TextInput(attrs={'class': 'input-xlarge'}),
            'end_rua': TextInput(attrs={'class': 'input-xlarge'}),
            'end_numero': TextInput(attrs={'class': 'input-mini'}),
            'end_complemento': TextInput(attrs={'placeholder': 'Complemento', 'class': 'input-small'}),
            'tel_1': TextInput(attrs={'placeholder': 'Ex: (xx) 0000-0000'}),
            'tel_1_ramal': TextInput(attrs={'class': 'input-mini', 'placeholder': 'Ramal'}),
            'tel_2': TextInput(attrs={'placeholder': 'Ex: (xx) 0000-0000'}),
            'tel_2_ramal': TextInput(attrs={'class': 'input-mini', 'placeholder': 'Ramal'}),
            'tel_fax': TextInput(attrs={'placeholder': 'Ex: (xx) 0000-0000'}),
            'valor_maximo_entrega': TextInput(attrs={'class': 'input-small mask-moeda'})
        }

class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        exclude = ('cliente','status_data')
        widgets = {
            'descricao': TextInput(attrs={'placeholder': 'Descrição', 'class': 'input-large'}),
            'status': HiddenInput(),
        }

ClienteProdutoFormSet = inlineformset_factory(Cliente, Produto, form=ProdutoForm, extra=1, can_delete=False)

class EntregadorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EntregadorForm, self).__init__(*args, **kwargs)
        self.fields['cidade_atendida'].queryset = Cidade.objects.filter(uf=u'RJ')

    class Meta:
        model = Entregador
        widgets = {
            'cpf_cnpj': TextInput(attrs={'class': 'input-medium'}),
            'nome': TextInput(attrs={'class': 'input-xlarge'}),
            'rg': TextInput(attrs={'class': 'input-large'}),
            'rg_expedicao': DateInput(attrs={'placeholder': '00/00/0000', 'class': 'input-small mask-data calendario_ui'}),
            'end_rua': TextInput(attrs={'class': 'input-xlarge'}),
            'end_numero': TextInput(attrs={'class': 'input-mini'}),
            'end_complemento': TextInput(attrs={'placeholder': 'Complemento', 'class': 'input-small'}),
            'end_bairro': TextInput(attrs={'class': 'input-large'}),
            'email': TextInput(attrs={'class': 'input-large'}),
            'tel_1': TextInput(attrs={'placeholder': 'Ex: (xx) 0000-0000'}),
            'tel_1_ramal': TextInput(attrs={'placeholder':'Ramal', 'class': 'input-mini'}),
            'tel_2': TextInput(attrs={'placeholder': 'Ex: (xx) 0000-0000'}),
            'tel_2_ramal': TextInput(attrs={'placeholder':'Ramal', 'class': 'input-mini'}),
            'tel_id_radio': TextInput(attrs={'class': 'input-mini'}),
            'agencia': TextInput(attrs={'class': 'input-mini'}),
            'agencia_dv': TextInput(attrs={'placeholder':'Dígito', 'class': 'input-mini'}),
            'conta': TextInput(attrs={'class': 'input-medium'}),
            'conta_dv': TextInput(attrs={'placeholder':'Dígito', 'class': 'input-mini'}),
            'pagamento_protocolo_valor': TextInput(attrs={'class': 'input-small mask-moeda'}),
            'valor_diaria': TextInput(attrs={'class': 'input-small mask-moeda'}),
            'valor_fixo': TextInput(attrs={'class': 'input-small mask-moeda'}),
            'obs': Textarea(attrs={'rows': 5})
        }

class EntregadorClienteForm(ModelForm):
    class Meta:
        model = EntregadorCliente
        widgets = {
            'valor': TextInput(attrs={'placeholder': 'Valor', 'class': 'input-small mask-moeda'})
        }

EntregadorClienteFormSet = inlineformset_factory(Entregador, EntregadorCliente, form=EntregadorClienteForm, extra=1, can_delete=True)

class LocomocaoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocomocaoForm, self).__init__(*args, **kwargs)
        self.fields['entregador'].queryset = Entregador.objects.filter(status=choices.STATUS_ATIVO).order_by('nome')
        
    class Meta:
        model = Locomocao
        exclude = ('mes_ref', 'ano_ref')
        widgets = {
            'valor': TextInput(attrs={'placeholder': 'Valor', 'class': 'input-small mask-moeda'}),
            'data_pagamento': DateInput(attrs={'placeholder': '00/00/0000','class': 'input-medium mask-data calendario_ui'}),
            'data_entrega_comprovante': DateInput(attrs={'placeholder': '00/00/0000','class': 'input-medium mask-data calendario_ui'}),
            'obs': Textarea(attrs={'rows': 5})
        }

class EntregaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EntregaForm, self).__init__(*args, **kwargs)
        self.fields['entregador'].queryset = Entregador.objects.filter(status=choices.STATUS_ATIVO).order_by('nome')

    class Meta:
        model = Entrega
        widgets = {
            'status': HiddenInput(),
            'saida_data': DateInput(attrs={'placeholder': '00/00/0000', 'class': 'input-medium mask-data calendario_ui'}),
            'retorno_data': DateInput(attrs={'placeholder': '00/00/0000', 'class': 'input-medium mask-data calendario_ui'}),
            'obs': Textarea(attrs={'rows': 5})
        }

class EntregaClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EntregaClienteForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.filter(status=choices.STATUS_ATIVO).order_by('razao_social')

    class Meta:
        model = EntregaCliente
        widgets = {
            'qtd_enviada': TextInput(attrs={'class': 'input-mini'}),
        }

class EntregaFormConsulta(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EntregaFormConsulta, self).__init__(*args, **kwargs)
        self.fields['entregador'].queryset = Entregador.objects.filter(status=choices.STATUS_ATIVO).order_by('nome')

    class Meta:
        model = Entrega
        widgets = {
            'entregador': HiddenInput(),
            'saida_data': HiddenInput(),
            'cliente': HiddenInput(),
            'retorno_data': DateInput(attrs={'placeholder': '00/00/0000', 'class': 'input-medium mask-data calendario_ui'}),
            'obs': Textarea(attrs={'rows': 5})
        }

class EntregaClienteFormConsulta(ModelForm):
    class Meta:
        model = EntregaCliente
        widgets = {
            'cliente': HiddenInput(),
            'qtd_enviada': HiddenInput(),
            'qtd_retorno': TextInput(attrs={'class': 'input-mini'}),
        }

EntregaClienteFormSet = inlineformset_factory(Entrega, EntregaCliente, form=EntregaClienteForm, extra=1, can_delete=False)
EntregaClienteFormSetConsulta = inlineformset_factory(Entrega, EntregaCliente, form=EntregaClienteFormConsulta, extra=0, can_delete=False)

class TransferenciaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransferenciaForm, self).__init__(*args, **kwargs)
        self.fields['entregador'].queryset = Entregador.objects.filter(status=choices.STATUS_ATIVO).order_by('nome')

    class Meta:
        model = Transferencia
        widgets = {
            'status': HiddenInput(),
            'saida_data': DateInput(attrs={'placeholder': '00/00/0000', 'class': 'input-medium mask-data calendario_ui'}),
            'retorno_data': DateInput(attrs={'placeholder': '00/00/0000', 'class': 'input-medium mask-data calendario_ui'}),
            'obs': Textarea(attrs={'rows': 5})
        }

class TransferenciaClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransferenciaClienteForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.filter(status=choices.STATUS_ATIVO).order_by('razao_social')

    class Meta:
        model = TransferenciaCliente
        widgets = {
            'qtd_enviada': TextInput(attrs={'class': 'input-mini'}),
        }

class TransferenciaFormConsulta(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransferenciaFormConsulta, self).__init__(*args, **kwargs)
        self.fields['entregador'].queryset = Entregador.objects.filter(status=choices.STATUS_ATIVO).order_by('nome')

    class Meta:
        model = Transferencia
        widgets = {
            'entregador': HiddenInput(),
            'saida_data': HiddenInput(),
            'destino': HiddenInput(),
            'retorno_data': DateInput(attrs={'placeholder': '00/00/0000', 'class': 'input-medium mask-data calendario_ui'}),
            'obs': Textarea(attrs={'rows': 5})
        }

class TransferenciaClienteFormConsulta(ModelForm):
    class Meta:
        model = TransferenciaCliente
        widgets = {
            'cliente': HiddenInput(),
            'qtd_enviada': HiddenInput(),
            'qtd_retorno': TextInput(attrs={'class': 'input-mini'}),
        }

TransferenciaClienteFormSet = inlineformset_factory(Transferencia, TransferenciaCliente, form=TransferenciaClienteForm, extra=1, can_delete=False)
TransferenciaClienteFormSetConsulta = inlineformset_factory(Transferencia, TransferenciaCliente, form=TransferenciaClienteFormConsulta, extra=0, can_delete=False)