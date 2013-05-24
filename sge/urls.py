# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from sge.source import views as vw

urlpatterns = patterns('',
	url(r'^$', 'django.contrib.auth.views.login', name='auth_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {"next_page": "/"}, name='auth_logout'),

    url(r'^mudar_senha/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'source/mudar_senha.html'}, name='source_mudar_senha'),
    url(r'^mudar_senha/concluido/$', 'django.contrib.auth.views.password_change_done',
        {'template_name': 'source/mudar_senha_concluido.html'}, name='source_mudar_senha_concluido'),

    url(r'^cidades-uf$', vw.CidadeListView.as_view(), name='source_cidades_uf'),
    url(r'^cliente/detail$', vw.ClienteDetailView.as_view(), name='source_cliente_detail'),
    url(r'^entregador/listar-clientes$', vw.EntregadorClienteListView.as_view(), name='source_entregador_cliente'),
    url(r'^entregador-cliente/valor$', vw.EntregadorClienteDetailView.as_view(), name='source_entregador_cliente_detail'),

	url(r'^painel-controle/$', vw.PainelControleView.as_view(), name='source_painel_controle'),
    url(r'^perfil/alteracao/(?P<pk>\d+)$', vw.PerfilEditarView.as_view(), name='source_perfil_alteracao'),

    url(r'^cliente/inclusao$', vw.ClienteInclusaoView.as_view(), name='source_cliente_inclusao'),
    url(r'^cliente/consulta$', vw.ClienteConsultaView.as_view(), name='source_cliente_consulta'),
    url(r'^cliente/alteracao/(?P<pk>\d+)$', vw.ClienteAlteracaoView.as_view(), name='source_cliente_alteracao'),
    url(r'^cliente/status-change/(?P<pk>\d+)/(?P<status>[0,1])$', vw.ClienteStatusChangeView.as_view(), name='source_cliente_status_change'),
    
    url(r'^entregador/inclusao$', vw.EntregadorInclusaoView.as_view(), name='source_entregador_inclusao'),
    url(r'^entregador/consulta$', vw.EntregadorConsultaView.as_view(), name='source_entregador_consulta'),
    url(r'^entregador/alteracao/(?P<pk>\d+)$', vw.EntregadorAlteracaoView.as_view(), name='source_entregador_alteracao'),
    url(r'^entregador/status-change/(?P<pk>\d+)/(?P<status>[0,1])$', vw.EntregadorStatusChangeView.as_view(), name='source_status_change'),

    url(r'^locomocao/inclusao$', vw.LocomocaoInclusaoView.as_view(), name='source_locomocao_inclusao'),
    url(r'^locomocao/consulta$', vw.LocomocaoConsultaView.as_view(), name='source_locomocao_consulta'),
    url(r'^locomocao/alteracao/(?P<pk>\d+)$', vw.LocomocaoAlteracaoView.as_view(), name='source_locomocao_alteracao'),
    url(r'^locomocao/pendente/(?P<pk>\d+)$', vw.LocomocaoPendenteView.as_view(), name='source_locomocao_pendente'),

    url(r'^entrega/inclusao$', vw.EntregaInclusaoView.as_view(), name='source_entrega_inclusao'),
    url(r'^entrega/consulta$', vw.EntregaConsultaView.as_view(), name='source_entrega_consulta'),
    url(r'^entrega/alteracao/(?P<pk>\d+)$', vw.EntregaAlteracaoView.as_view(), name='source_entrega_alteracao'),
    url(r'^entrega/cancelar/(?P<pk>\d+)$', vw.EntregaCancelamentoView.as_view(), name='source_entrega_cancelamento'),

    url(r'^transferencia/inclusao$', vw.TransferenciaInclusaoView.as_view(), name='source_transferencia_inclusao'),
    url(r'^transferencia/consulta$', vw.TransferenciaConsultaView.as_view(), name='source_transferencia_consulta'),
    url(r'^transferencia/alteracao/(?P<pk>\d+)$', vw.TransferenciaAlteracaoView.as_view(), name='source_transferencia_alteracao'),
    url(r'^transferencia/cancelar/(?P<pk>\d+)$', vw.TransferenciaCancelamentoView.as_view(), name='source_transferencia_cancelamento'),
)
