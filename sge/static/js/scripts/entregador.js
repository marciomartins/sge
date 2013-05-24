/*
 * Máscaras
 ******************************************************************************/
if ($('.mask-moeda').length || $('.mask-data').length) {
	$('.mask-data').mask(mascaras.data);
	$('.mask-moeda').priceFormat(cfgPriceFormat);
}
$('.calendario_ui').datepicker(cfgCalendario);

/*
 * Bloqueia campos do form de acordo com o tipo de entregador, tipo da entraga, 
 * pagamento de protocolo.
 ******************************************************************************/
tratar_cidade_atendida();
function tratar_cidade_atendida() {
	switch ($('#id_tipo_entregador').val()) {
	case 'cpf':
		$('#id_cidade_atendida').attr('disabled', true);
		$('#id_rg').attr('disabled', false);
		$('#id_rg_expedicao').attr('disabled', false);
		$('#id_cpf_cnpj').unmask().mask(mascaras.cpf);
		break
	case 'cnpj':
		$('#id_cidade_atendida').attr('disabled', false);
		$('#id_rg').val('').attr('disabled', true);
		$('#id_rg_expedicao').val('').attr('disabled', true);
		$('#id_cpf_cnpj').unmask().mask(mascaras.cnpj);
		break
	default:
		$('#id_cpf_cnpj').unmask();
		$('form').find("input[type=text], textarea").attr('disabled', false);
	}
}
$('#id_tipo_entregador').on('change', tratar_cidade_atendida);

tratar_tipo_entrega();
function tratar_tipo_entrega() {
	if ($('#id_tipo_entraga').val() === 'sub_base') {
		$('#id_pagamento_protocolo').attr('disabled', false);
	} else {
        $('#id_pagamento_protocolo').attr('checked', false).attr('disabled', true);
		$('#id_pagamento_protocolo_valor').attr('disabled', true);
	}	
}
$('#id_tipo_entraga').on('change', tratar_tipo_entrega);

tratar_pagamento_protocolo();
function tratar_pagamento_protocolo() {
	if ($('#id_pagamento_protocolo').is(':checked')) {
		$('#id_pagamento_protocolo_valor').attr('disabled', false);
	} else {
		$('#id_pagamento_protocolo_valor').val('').attr('disabled', true);
	}	
}
$('#id_pagamento_protocolo').on('change', tratar_pagamento_protocolo);

tratar_categoria_entregador();
function tratar_categoria_entregador() {
	switch ($('#id_categoria_entregador').val()) {
	case 'diaria_com_entrega':
		$('#clientes').fadeIn();
        $('#id_valor_diaria').attr('disabled', false);
        $('#id_valor_fixo').attr('disabled', true).val('');
		break
	case 'diaria_por_entrega':
		$('#clientes').fadeIn();
        $('#id_valor_diaria').attr('disabled', false);
        $('#id_valor_fixo').attr('disabled', true).val('');
		break
    case 'fixo_com_entrega':
        $('#clientes').fadeIn();
        $('#id_valor_diaria').attr('disabled', true).val('');
        $('#id_valor_fixo').attr('disabled', false);
        break
	case 'fixo_sem_entrega':
		$('#clientes').hide();
        $('#id_valor_diaria').attr('disabled', true).val('');
        $('#id_valor_fixo').attr('disabled', false);
        break
    default:
        $('#clientes').hide();
        $('#id_valor_diaria').attr('disabled', false).val('');
        $('#id_valor_fixo').attr('disabled', false).val('');
	}
}
$('#id_categoria_entregador').on('change', tratar_categoria_entregador);

/*
 * Carrega cidades por estado
 ******************************************************************************/
handle_cidades_uf($('#id_end_estado'), $('#id_end_cidade'), '/cidades-uf', 'codigo_cidade', 'nome', '---------');

/*
 * Adiciona clientes
 ******************************************************************************/
$('#bt-adicionar-cliente').on('click', function() {
    var tb_produtos = $('#tb-clientes > tbody');
    var clone = tb_produtos.find('tr:first').clone('true');
    var total = parseInt($('#id_entregadorcliente_set-TOTAL_FORMS').val(), 10);
    var new_order_num = parseInt($('#tb-clientes > tbody tr:last :text[name ^= entregadorcliente_set-]:first').attr('name').split('-')[1], 10)+1;
    clone.appendTo(tb_produtos).fadeIn();

    clone.find(':checkbox').attr('checked', false);
    clone.find('.control-group.error').removeClass('error');
    clone.find('.help-inline').hide();
    clone.find(':text, select').val('');
    clone.find(':hidden[name $= -id]').val('');
    clone.find(':text[name $= -valor]').priceFormat(cfgPriceFormat);
    clone.find(':text:first').focus();
    clone.find('span.valor-maximo-entrega-cliente').removeClass('label-important').addClass('label-info').hide();
    clone.find(':hidden.valor-maximo-entrega-cliente-hd').val('');

    reordenar_clientes();
    $('#id_entregadorcliente_set-TOTAL_FORMS').val(total+1);
    estilizar_linhas();
});

function reordenar_clientes() {
    // Altera attr name e id com nova ordem
    var current_name, new_id, new_name;
    
    $('#tb-clientes > tbody tr').each(function(i) {
        $(this).find('[id ^= id_entregadorcliente_set-]').each(function(){
            current_name = $(this).attr('name');
            new_name = current_name.split('-')[0]+'-'+i+'-'+current_name.split('-').slice(2).join('-');
            new_id = 'id_'+new_name;
            $(this).attr('id', new_id).attr('name', new_name);
        });
    });
}

/*
 * Remove clientes
 ******************************************************************************/
$('#tb-clientes .icon-trash').on('click', function(e){
    var dlg_txt = '<p>Você tem certeza que deseja remover este cliente?</p>';
    e.preventDefault();
    $('#dlg-confirm .modal-body').html(dlg_txt);
    $('#dlg-confirm').data('opener', $(this).closest('tr')).modal('show');
});
$('#bt-confirm').on('click', function(e){
    e.preventDefault();
    var opener = $('#dlg-confirm').data('opener');
    var total = parseInt($('#id_entregadorcliente_set-TOTAL_FORMS').val(), 10);

    if (total === 1) {
        $('#bt-adicionar-cliente').click();
        total = parseInt($('#id_entregadorcliente_set-TOTAL_FORMS').val(), 10);
    }

    if (opener.find(':hidden[name $= -id]').val() == '') {
        opener.remove();
        reordenar_clientes();
        $('#id_entregadorcliente_set-TOTAL_FORMS').val(total-1);
    } else {
        opener.hide().find(':checkbox[name $= -DELETE]').attr('checked', true);
    }

    $('#dlg-confirm').modal('hide');
    estilizar_linhas();
});

/*
 * Mostra o valor máximo para cada cliente
 ******************************************************************************/
$('#clientes select[name $= -cliente]').on('change', function(){
    var label = $(this).closest('tr').find('span.valor-maximo-entrega-cliente');
    var field = $(this).closest('tr').find(':hidden.valor-maximo-entrega-cliente-hd');
	if ($(this).val()) {
	    $.get('/cliente/detail', {pk: $(this).val()}, function(data) {
	        label.html('Valor máximo: R$ ' + data.object.valor_maximo_entrega).fadeIn().removeClass('label-important').addClass('label-info');
            field.val(data.object.valor_maximo_entrega);
	    }, 'json');
	} else {
        label.html("").hide();
        field.val("");
    }
});
$('#clientes select[name $= -cliente]').change();

/*
 * Estiliza linhas da lista de clientes
 ******************************************************************************/
function estilizar_linhas() {
    $('#clientes table tr:visible:odd td').css('background-color', '#f9f9f9');
}
$('#clientes table tr:odd td').css('background-color', '#f9f9f9');

/*
 * Verifica se existe "validation error" no formulário
 ******************************************************************************/
if ($('#tab-pane-navegation .error')) {
	var tab_erro = $('#tab-pane-navegation .error:first').closest('.tab-pane').attr('id');
	$('#tab-'+tab_erro).find('a').tab('show');
}

/*
 * Esconde checkboxes DELETE
 ******************************************************************************/
$('#tb-clientes :checkbox[name $= -DELETE]').hide();

/*
 * Link para tela de alterção
 ******************************************************************************/
$('#tb-entregador-consulta > tbody > tr td:not(.status)').on('click', function(){
	location.href = $(this).parent().attr('url-edit');
});

$('.no-action').on('click', function(){
    location.href = '/entregador/consulta';
});

/*
 * Muda o status do entregador
 ******************************************************************************/
$('.desactivate .status').on('click', function(){
	var url = $(this).parent().attr('url-status-change');
	var entregador_nome =  $(this).parent().find('.entregador_nome').text();
	$('#desativar-entregador .modal-body').html('<p>Você tem certeza que deseja desativar o entregador <strong>'+entregador_nome+'?</strong></p>');
	$('#bt-action').removeClass('btn-success').addClass('btn-danger').attr('href', url);
	$('#desativar-entregador').modal('show');
});
$('.activate .status').on('click', function(){
	var url = $(this).parent().attr('url-status-change');
	var entregador_nome =  $(this).parent().find('.entregador_nome').text();
	$('#desativar-entregador .modal-body').html('<p>Você tem certeza que deseja reativar o entregador <strong>'+entregador_nome+'?</strong></p>');
	$('#bt-action').removeClass('btn-danger').addClass('btn-success').attr('href', url);
	$('#desativar-entregador').modal('show');
});