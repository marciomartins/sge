/*
 * Máscaras
 ******************************************************************************/
$('.mask-data').mask(mascaras.data);
$('.calendario_ui').datepicker(cfgCalendario);

/*
 * Carrega os clientes associados ao entregador
 ******************************************************************************/
$('select#id_entregador').on('change', function(){
    var id_entregador = $.trim($(this).val());
    var html_opt = '';
    var current_val;

    if (id_entregador.length) {
        $.get('/entregador/listar-clientes', {pk: $(this).val()}, function(data) {
            html_opt = populate_combo(data.object_list, 'id', 'nome', '---------');
            $('#tb-clientes select[name $= -cliente]').each(function(){
                current_val = $(this).val();
                $(this).html(html_opt).val(current_val).closest('tr').find(':text').val('');
            });
        }, 'json');
    } else {
        html_opt = populate_combo([], 'id', 'nome', '---------');
        $('#tb-clientes select[name $= -cliente]').each(function(){
            $(this).html(html_opt).val('').closest('tr').find(':text').val('');
        });
    }
});
$('select#id_entregador').change();

/*
 * Adiciona cliente
 ******************************************************************************/
$('#bt-adicionar-linha-cliente').on('click', function(){
    var tb_clientes = $('#tb-clientes > tbody');
    var clone = tb_clientes.find('tr:first').clone('true');
    var total = parseInt($('#id_transferenciacliente_set-TOTAL_FORMS').val(), 10);
    var new_order_num = parseInt($('#tb-clientes > tbody tr:last :text[name ^= transferenciacliente_set-]:first').attr('name').split('-')[1], 10)+1;
    
    clone.appendTo(tb_clientes).fadeIn();

    clone.find('.control-group.error').removeClass('error');
    clone.find('.help-inline').hide();
    clone.find(':text').val('0');
    clone.find('select').val('');
    clone.find(':hidden[name $= -id]').val('');
    clone.find(':text:first').focus();

    reordenar_campos_cliente();
    $('#id_transferenciacliente_set-TOTAL_FORMS').val(total+1);
    estilizar_linhas();
});
function reordenar_campos_cliente() {
    var current_name, new_id, new_name;
    
    $('#tb-clientes > tbody tr').each(function(i) {
        $(this).find('[id ^= id_transferenciacliente_set-]').each(function(){
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
    var dlg_txt = '<p>Você tem certeza que deseja remover este cliente ?</p>';
    e.preventDefault();
    $('#dlg-confirm .modal-body').html(dlg_txt);
    $('#dlg-confirm').data('opener', $(this).closest('tr')).modal('show');
});
$('#bt-confirm').on('click', function(e){
    e.preventDefault();
    var opener = $('#dlg-confirm').data('opener');
    var total = parseInt($('#id_transferenciacliente_set-TOTAL_FORMS').val(), 10);

    if (total === 1) {
        $('#bt-adicionar-linha-cliente').click();
        total = parseInt($('#id_transferenciacliente_set-TOTAL_FORMS').val(), 10);
    }

    opener.remove();
    reordenar_campos_cliente();
    $('#id_transferenciacliente_set-TOTAL_FORMS').val(total-1);
    
    $('#dlg-confirm').modal('hide');
    estilizar_linhas();
});

/*
 * Estiliza linhas da lista de clientes
 ******************************************************************************/
function estilizar_linhas() {
    $('#clientes table tr:visible:odd td').css('background-color', '#f9f9f9');
    $('#clientes table tr:visible:even td').css('background-color', '#ffffff');
}
$('#clientes table tr:odd td').css('background-color', '#f9f9f9');
$('#clientes table tr:even td').css('background-color', '#ffffff');

/*
 * Verifica se existe "validation error" no formulário
 ******************************************************************************/
if ($('#tab-pane-navegation .error')) {
    var tab_erro = $('#tab-pane-navegation .error:first').closest('.tab-pane').attr('id');
    $('#tab-'+tab_erro).find('a').tab('show');
}

/*
 * Mostra tela de alterção
 ******************************************************************************/
$('#tb-entrega-consulta > tbody > tr td:not(.cancel)').on('click', function(){
    location.href = $(this).parent().attr('url-edit');
});
$('.no-action').on('click', function(){
    location.href = '/transferencia/consulta';
});

/*
 * Cancelar transferencia
 ******************************************************************************/
 $('.cancel').on('click', function(){
    var url = $(this).parent().attr('url-cancel');
    var entregador_nome = $(this).parent().find('.entregador_nome').text();
    var entrega_saida = $(this).parent().find('.transferencia_saida').text();
    $('#confirm-cancel-entrega .modal-body')
        .html('<p>Você tem certeza que deseja cancelar a transferência selecionada ?</p> <p>Entrega de: <strong>'+entregador_nome+'</strong> Enviada em: <strong>'+entrega_saida+'</strong></p>');
    $('#bt-confirm-cancel-entrega').attr('href', url);
    $('#confirm-cancel-entrega').modal('show');
 });