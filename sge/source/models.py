# -*- coding: utf-8 -*-

import choices

from datetime import date
from decimal import Decimal

from django.db import models

__all__ = ('Cidade', 'Cliente', 'Produto', 'Entregador',
		   'EntregadorCliente', 'Locomocao', 'Entrega',
		   'EntregaCliente', 'Transferencia', 'TransferenciaCliente')


class CurrencyField(models.DecimalField):
	__metaclass__ = models.SubfieldBase

	def to_python(self, value):
		try:
			return super(CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
		except AttributeError:
			return None


class Cidade(models.Model):
	codigo_cidade =  models.CharField(primary_key=True, max_length=10, verbose_name='Código do município')
	uf = models.CharField(max_length=2, verbose_name='UF da cidade', choices=choices.ESTADOS)
	nome = models.CharField(max_length=200, verbose_name='Nome da cidade')

	def __unicode__(self):
		return self.nome


class Cliente(models.Model):
	cnpj = models.CharField(max_length=20, verbose_name='CNPJ', blank=True, null=True)
	razao_social = models.CharField(max_length=120, verbose_name='Razão social')
	end_rua = models.CharField(max_length=120, verbose_name='Logradouro')
	end_numero = models.CharField(max_length=10, verbose_name='Número', blank=True, null=True)
	end_complemento = models.CharField(max_length=100, verbose_name='Complemento', blank=True, null=True)
	end_bairro = models.CharField(max_length=80, verbose_name='Bairro', blank=True, null=True)
	end_estado = models.CharField(max_length=2, verbose_name='Estado', choices=choices.ESTADOS)
	end_cidade = models.ForeignKey(Cidade, verbose_name='Cidade', blank=True, null=True)
	email = models.CharField(max_length=60, verbose_name='E-mail', blank=True, null=True)
	tel_1 = models.CharField(max_length=20, verbose_name='Telefone')
	tel_1_ramal = models.CharField(max_length=10, verbose_name='Ramal', blank=True, null=True)
	tel_2 = models.CharField(max_length=20, verbose_name='Telefone 2', blank=True, null=True)
	tel_2_ramal = models.CharField(max_length=10, verbose_name='Ramal 2', blank=True, null=True)
	tel_fax = models.CharField(max_length=20, verbose_name='Fax',blank=True, null=True)
	valor_maximo_entrega = CurrencyField(max_digits=5,  verbose_name='Valor máximo por entrega', decimal_places=2)
	obs = models.CharField(max_length=200, verbose_name='Obs', blank=True, null=True)
	status = models.IntegerField(max_length=1, verbose_name='Situação', choices=choices.STATUS, default=choices.STATUS_ATIVO)
	status_data = models.DateField(verbose_name='Data situação', blank=True, null=True)

	def produtos_ativos(self):
		return self.produto_set.filter(status=choices.STATUS_ATIVO).order_by('descricao')

	def __unicode__(self):
		return self.razao_social


class Produto(models.Model):
	cliente = models.ForeignKey(Cliente)
	descricao = models.CharField(max_length=120, verbose_name='Descrição')
	status = models.IntegerField(max_length=1, verbose_name='Situação', choices=choices.STATUS, default=choices.STATUS_ATIVO)
	status_data = models.DateField(verbose_name='Data situação', blank=True, null=True)

	def __unicode__(self):
		return self.descricao


class Entregador(models.Model):
	tipo_entregador = models.CharField(max_length=20, verbose_name='Tipo entregador', choices=choices.TIPO_ENTREGADOR)
	cpf_cnpj = models.CharField(max_length=20, verbose_name='CPF/CNPJ')
	nome = models.CharField(max_length=120, verbose_name='Nome/Razão social')
	rg = models.CharField(max_length=20, verbose_name='RG', blank=True, null=True)
	rg_expedicao = models.DateField(verbose_name='Expedição', blank=True, null=True)
	end_rua = models.CharField(max_length=120, verbose_name='Logradouro')
	end_numero = models.CharField(max_length=10, verbose_name='Número', blank=True, null=True)
	end_complemento = models.CharField(max_length=100, verbose_name='Complemento', blank=True, null=True)
	end_bairro = models.CharField(max_length=80, verbose_name='Bairro', blank=True, null=True)
	end_estado = models.CharField(max_length=2, verbose_name='Estado', choices=choices.ESTADOS)
	end_cidade = models.ForeignKey(Cidade, verbose_name='Cidade', blank=True, null=True)
	email = models.CharField(max_length=60, verbose_name='E-mail', blank=True, null=True)
	tel_1 = models.CharField(max_length=20, verbose_name='Telefone')
	tel_1_ramal = models.CharField(max_length=10, verbose_name='Ramal', blank=True, null=True)
	tel_2 = models.CharField(max_length=20, verbose_name='Telefone 2', blank=True, null=True)
	tel_2_ramal = models.CharField(max_length=10, verbose_name='Ramal 2', blank=True, null=True)
	tel_id_radio = models.CharField(max_length=10, verbose_name='ID Nextel', blank=True, null=True)
	banco = models.CharField(max_length=10, verbose_name='Banco', choices=choices.BANCOS)
	agencia = models.CharField(max_length=10, verbose_name='Agência')
	agencia_dv = models.CharField(max_length=4, verbose_name='Agência DV', blank=True, null=True)
	conta = models.CharField(max_length=20, verbose_name='Conta')
	conta_dv = models.CharField(max_length=4, verbose_name='Conta DV', blank=True, null=True)
	categoria_entregador = models.CharField(max_length=80, verbose_name='Categoria entregador', choices=choices.CATEGORIA_ENTREGADOR)
	tipo_entraga = models.CharField(max_length=20, verbose_name='Tipo de entrega', choices=choices.TIPO_ENTREGA)
	pagamento_protocolo = models.BooleanField(verbose_name='Protocolo?', default=False)
	pagamento_protocolo_valor = CurrencyField(max_digits=10,  verbose_name='Valor do protocolo', decimal_places=2, blank=True, null=True)
	cidade_atendida = models.ForeignKey(Cidade, related_name='entregador_atendido', verbose_name='Cidade atendida', blank=True, null=True)
	valor_fixo = CurrencyField(max_digits=10, verbose_name='Valor fixo', decimal_places=2, blank=True, null=True)
	valor_diaria = CurrencyField(max_digits=10, verbose_name='Valor diária', decimal_places=2, blank=True, null=True)
	status = models.IntegerField(max_length=1, verbose_name='Situação', choices=choices.STATUS, default=choices.STATUS_ATIVO)
	status_data = models.DateField(verbose_name='Data situação', blank=True, null=True)
	obs = models.CharField(max_length=200, verbose_name='Obs', blank=True, null=True)

	def __unicode__(self):
		return self.nome


class EntregadorCliente(models.Model):
	entregador = models.ForeignKey(Entregador)
	cliente = models.ForeignKey(Cliente)
	valor = CurrencyField(max_digits=10, verbose_name='Valor', decimal_places=2)

	def __unicode__(self):
		return u'Entregador: {}, Cliente: {}, Valor: {}'.format(self.entregador.nome, self.cliente.razao_social, self.valor)


class Locomocao(models.Model):
	entregador = models.ForeignKey(Entregador)
	tipo_locomocao = models.CharField(max_length=20,verbose_name='Tipo de locomoção', choices=choices.TIPO_LOCOMOCAO)
	combustivel = models.CharField(max_length=20, verbose_name='Combustível', choices=choices.COMBUSTIVEL, blank=True, null=True)
	valor = CurrencyField(max_digits=10, verbose_name='Valor', decimal_places=2)
	mes_ref = models.IntegerField(max_length=2, default=date.today().month)
	ano_ref = models.IntegerField(max_length=4,  default=date.today().year)
	data_pagamento = models.DateField(verbose_name='Data pagamento')
	data_entrega_comprovante = models.DateField(verbose_name='Data entrega da nota', blank=True, null=True)
	situacao_comprovante = models.CharField(max_length=20,verbose_name='Comprovante', choices=choices.STATUS_LOCOMOCAO, default='comp_pendente')
	obs = models.CharField(max_length=200, verbose_name='Obs', blank=True, null=True)

	def __unicode__(self):
		return u'Entegador: {}, Tipo: {}, Combustivel: {}, Valor: {}'.format(self.entregador.nome, self.tipo_locomocao, self.combustivel, self.valor)


class Entrega(models.Model):
	entregador = models.ForeignKey(Entregador)
	saida_data = models.DateField(verbose_name='Data saída', default=date.today())
	retorno_data = models.DateField(verbose_name='Data retorno', blank=True, null=True)
	status = models.CharField(max_length=20, verbose_name='Status da entrega', default=choices.STATUS_ENTREGA[0][0], choices=choices.STATUS_ENTREGA)
	obs = models.CharField(max_length=200, verbose_name='Obs', blank=True, null=True)

	def valor(self):
		valor_total = 0.0
		if self.entregador.categoria_entregador != u'fixo_sem_entrega':
			for entrega_cliente in self.entregacliente_set.all():
				valor = 0.0
				qtd_retorno = entrega_cliente.qtd_retorno if entrega_cliente.qtd_retorno else 0
				qtd = entrega_cliente.qtd_enviada - qtd_retorno

				entregador_cliente = self.entregador.entregadorcliente_set.get(cliente=entrega_cliente.cliente)
				if entregador_cliente:
					valor_total += qtd * float(entregador_cliente.valor)
		return valor_total


class EntregaCliente(models.Model):
	entrega = models.ForeignKey(Entrega)
	cliente = models.ForeignKey(Cliente)
	qtd_enviada = models.IntegerField(max_length=5)
	qtd_retorno = models.IntegerField(max_length=5, default=0, blank=True, null=True)

	def __unicode__(self):
		return u'{} ({})'.format(self.cliente.razao_social, self.qtd_enviada)


class Transferencia(models.Model):
	entregador = models.ForeignKey(Entregador)
	saida_data = models.DateField(verbose_name='Data saída', default=date.today())
	retorno_data = models.DateField(verbose_name='Data retorno', blank=True, null=True)
	destino = models.CharField(max_length=20, verbose_name='Destino', choices=choices.DESTINO_TRANSFERENCIA)
	status = models.CharField(max_length=20, verbose_name='Status da entrega', default=choices.STATUS_ENTREGA[0][0], choices=choices.STATUS_ENTREGA)
	obs = models.CharField(max_length=200, verbose_name='Obs', blank=True, null=True)

	def valor(self):
		valor_total = 0.0
		if self.entregador.categoria_entregador != u'fixo_sem_entrega':
			for transferencia_cliente in self.transferenciacliente_set.all():
				valor = 0.0
				qtd_retorno = transferencia_cliente.qtd_retorno if transferencia_cliente.qtd_retorno else 0
				qtd = transferencia_cliente.qtd_enviada - qtd_retorno

				entregador_cliente = self.entregador.entregadorcliente_set.get(cliente=transferencia_cliente.cliente)
				if entregador_cliente:
					valor_total += qtd * float(entregador_cliente.valor)
		return valor_total


class TransferenciaCliente(models.Model):
	transferencia = models.ForeignKey(Transferencia)
	cliente = models.ForeignKey(Cliente)
	qtd_enviada = models.IntegerField(max_length=5)
	qtd_retorno = models.IntegerField(max_length=5, default=0, blank=True, null=True)

	def __unicode__(self):
		return u'{} ({})'.format(self.cliente.razao_social, self.qtd_enviada)