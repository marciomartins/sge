# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

MENU_PRINCIPAL = [
	[u'Painel de controle', u'source_painel_controle', None],
    [u'Entregas', u'', [
            [u'Atribuir', u'source_entrega_inclusao', None],
            [u'Consultar', u'source_entrega_consulta', None]
        ]
    ],
    [u'Transferência', u'', [
            [u'Atribuir', u'source_transferencia_inclusao', None],
            [u'Consultar', u'source_transferencia_consulta', None]
        ]
    ],
    [u'Locomoção', u'', [
            [u'Gerar', u'source_locomocao_inclusao', None],
            [u'Consultar', u'source_locomocao_consulta', None]
        ]
    ],
	[u'Entregadores', u'', [
    		[u'Incluir', u'source_entregador_inclusao', None],
            [u'Consultar', u'source_entregador_consulta', None]
        ]
	],
    [u'Clientes', u'', [
            [u'Incluir', u'source_cliente_inclusao', None],
            [u'Consultar', u'source_cliente_consulta', None]
        ]
    ],
	[u'Relatórios', u'', [
		  [u'Fechamento mensal de entregadores', u'', None],
        ]
	]
]

STATUS_ATIVO = 1
STATUS_INATIVO = 0
STATUS = (
    (STATUS_ATIVO, 'Ativo'),
    (STATUS_INATIVO, 'Inativo'),
)

FLG_SIM = 1
FLG_NAO = 0
FLG_SIM_NAO = (
    (FLG_SIM, 'Sim'),
    (FLG_NAO, 'Não'),
)

BANCOS = (
	(u'001', u'Banco do Brasil'),
	(u'237', u'Bradesco'),
	(u'104', u'Caixa Econômica Federal'),
	(u'745', u'Citibank'),
	(u'399', u'HSBC Bank Brasil S.A. - Banco Múltiplo'),
	(u'341', u'Itaú Unibanco S.A.'),
	(u'151', u'Nossa caixa'),
	(u'356', u'Real'),
	(u'033', u'Santander')
)

ESTADOS = (
    (u'AC', u'Acre'),
    (u'AL', u'Alagoas'),
    (u'AP', u'Amapá'),
    (u'AM', u'Amazonas'),
    (u'BA', u'Bahia'),
    (u'CE', u'Ceará'),
    (u'DF', u'Distrito Federal'),
    (u'ES', u'Espírito Santo'),
    (u'GO', u'Goiás'),
    (u'MT', u'Mato Grosso'),
    (u'MA', u'Maranhão'),
    (u'MS', u'Mato Grosso do Sul'),
    (u'MG', u'Minas Gerais'),
    (u'PA', u'Pará'),
    (u'PB', u'Paraíba'),
    (u'PR', u'Paraná'),
    (u'PE', u'Pernambuco'),
    (u'PI', u'Piauí'),
    (u'RJ', u'Rio de Janeiro'),
    (u'RN', u'Rio Grande do Norte'),
    (u'RS', u'Rio Grande do Sul'),
    (u'RO', u'Rondônia'),
    (u'RR', u'Roraima'),
    (u'SC', u'Santa Catarina'),
    (u'SP', u'São Paulo'),
    (u'SE', u'Sergipe'),
    (u'TO', u'Tocantins')
)

DESTINO_TRANSFERENCIA = (
    (u'nova_friburgo', u'Nova Friburgo'),
    (u'macae', u'Macaé'),
    (u'petropolis', u'Petropolis'),
    (u'volta_redonda', u'Volta redonda'),
    (u'campos', u'Campos')
)

TIPO_ENTREGADOR = (
	(u'cpf', u'CPF'),
	(u'cnpj', u'CNPJ')
)

TIPO_ENTREGA = (
	(u'moto', u'Moto dibra'),
	(u'ape', u'Apé dibra'),
	(u'block', u'Blockbuster'),
	(u'sub_base', u'Sub-base')
)

TIPO_LOCOMOCAO = (
	(u'passagem', u'Passagem'),
	(u'combustivel', u'Combustível')
)

STATUS_LOCOMOCAO = (
    (u'comp_pendente', 'Pendente'),
    (u'comp_nao_entregue', 'Não entregue'),
    (u'comp_entregue', 'Entregue'),
)

COMBUSTIVEL = (
	(u'gasolina', u'Gasolina'),
	(u'alcool', u'Álcool'),
	(u'diesel', u'Diesel'),
	(u'gnv', u'GNV')
)

CATEGORIA_ENTREGADOR = (
    (u'diaria_com_entrega', u'Diária com entrega'),
	(u'diaria_por_entrega', u'Diária por entrega'),
	(u'fixo_com_entrega', u'Fixo com entrega'),
    (u'fixo_sem_entrega', u'Fixo sem entrega')
)

STATUS_ENTREGA = (
	(u'enviada', 'Atribuido'),
	(u'entregue', 'Entregue'),
    (u'parc_entregue', 'Parcialmente entregue'),
    (u'devolvida', 'Devolvida'),
	(u'cancelada', 'Cancelada')
)