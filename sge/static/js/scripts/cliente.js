/*
 * Máscaras
 ******************************************************************************/
if ($('.mask-cnpj').length || $('.mask-moeda').length) {
    $('.mask-cnpj').mask(mascaras.cnpj);
    $('.mask-moeda').priceFormat(cfgPriceFormat);
}

/*
 * Carrega cidade por estado
 ******************************************************************************/
handle_cidades_uf($('#id_end_estado'), $('#id_end_cidade'), '/cidades-uf', 'codigo_cidade', 'nome', '---------');

/*
 * Adiciona produtos
 ******************************************************************************/
$('#bt-adicionar-linha-produto').on('click', function() {
    var tb_produtos = $('#tb-produtos > tbody');
    var clone = tb_produtos.find('tr:first').clone('true');
    var total = parseInt($('#id_produto_set-TOTAL_FORMS').val(), 10);
    var new_order_num = parseInt($('#tb-produtos > tbody tr:last :text[name ^= produto_set-]:first').attr('name').split('-')[1], 10)+1;
    
    clone.appendTo(tb_produtos).fadeIn();

    clone.find(':text').val('');
    clone.find(':hidden[name $= -id]').val('');
    clone.find(':hidden[name $= -status]').val(1); // O status de um produto novo deve ser ativo
    clone.find(':text:first').focus();

    reordenar_campos_produto();
    $('#id_produto_set-TOTAL_FORMS').val(total+1);
    estilizar_linhas();
});

/*
 * Remove produtos
 ******************************************************************************/
$('#tb-produtos .icon-trash').on('click', function(e){
    e.preventDefault();
    $('#dlg-confirm-remover-produto').data('opener', $(this).closest('tr')).modal('show');
});
$('#bt-remover-produto').on('click', function(e){
    e.preventDefault();
    var opener = $('#dlg-confirm-remover-produto').data('opener');
    var total = parseInt($('#id_produto_set-TOTAL_FORMS').val(), 10);

    if (total === 1) {
        $('#bt-adicionar-linha-produto').click();
        total = parseInt($('#id_produto_set-TOTAL_FORMS').val(), 10);
    }

    if (opener.find(':hidden[name $= -id]').val() == '') {
        opener.remove();
        reordenar_campos_produto();
        $('#id_produto_set-TOTAL_FORMS').val(total-1);
    } else {
        opener.hide().find(':hidden[name $= -status]').val(0);
    }
    
    $('#dlg-confirm-remover-produto').modal('hide');
    estilizar_linhas();
});

function reordenar_campos_produto() {
    // Altera attr name e id com nova ordem
    var current_name, new_id, new_name;
    
    $('#tb-produtos > tbody tr').each(function(i) {
        $(this).find('[id ^= id_produto_set-]').each(function(){
            current_name = $(this).attr('name');
            new_name = current_name.split('-')[0]+'-'+i+'-'+current_name.split('-').slice(2).join('-');
            new_id = 'id_'+new_name;

            $(this).attr('id', new_id).attr('name', new_name);
        });
    });
}

/*
 * Estiliza linhas da lista de produtos
 ******************************************************************************/
function estilizar_linhas() {
    $('#produtos table tr:visible:odd td').css('background-color', '#f9f9f9');
}
$('#produtos table tr:odd td').css('background-color', '#f9f9f9');

/*
 * Esconde os produtos inativos
 ******************************************************************************/
$('#produtos :hidden[name $= -status][value = 0]').closest('tr').hide();

/*
 * Verifica se existe "validation erro" no formulário
 ******************************************************************************/
if ($('#tab-pane-navegation .error')) {
    var tab_erro = $('#tab-pane-navegation .error:first').closest('.tab-pane').attr('id');
    $('#tab-'+tab_erro).find('a').tab('show');
}

/*
 * Link para tela de alterção
 ******************************************************************************/
$('#tb-cliente-consulta > tbody > tr td:not(.status)').on('click', function(){
    location.href = $(this).parent().attr('url-edit');
});

/*
 * Muda o status do entrega
 ******************************************************************************/
$('.desactivate .status').on('click', function(){
    var url = $(this).parent().attr('url-status-change');
    var cliente_nome =  $(this).parent().find('.cliente_nome').text();
    $('#confirm .modal-body').html('<p>Você tem certeza que deseja desativar o cliente <strong>'+cliente_nome+'?</strong></p>');
    $('#bt-confirm').removeClass('btn-success').addClass('btn-danger').attr('href', url);
    $('#confirm').modal('show');
});
$('.activate .status').on('click', function(){
    var url = $(this).parent().attr('url-status-change');
    var cliente_nome =  $(this).parent().find('.cliente_nome').text();
    $('#confirm .modal-body').html('<p>Você tem certeza que deseja reativar o cliente <strong>'+cliente_nome+'?</strong></p>');
    $('#bt-confirm').removeClass('btn-danger').addClass('btn-success').attr('href', url);
    $('#confirm').modal('show');
});