/* 
 * Variáveis globais do sistema
 ******************************************************************************/
 var mascaras = {
    telefone:'(99) 9999-9999', 
    cep:'99999-999', 
    cpf:'999.999.999-99', 
    cnpj:'99.999.999/9999-99', 
    data:'99/99/9999'
}
var cfgCalendario = {
    dateFormat: 'dd/mm/yy',
    dayNamesMin: ['D', 'S', 'T', 'Q', 'Q', 'S', 'S'],
    monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
    dayNamesShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'],
    showOtherMonths: true,
    selectOtherMonths: true    
}

var cfgPriceFormat = {
    prefix: '', centsSeparator: '.', thousandsSeparator: ''
}

$('.mask-moeda').on('blur', function(){
    var valor = $(this).val();
    valor = valor.replace(',','').replace('.','');
    valor = parseInt(valor,10);
    if (!valor) {
        $(this).val('');
    }
});

function handle_cidades_uf(field_uf, field_cidade, url, attr_value, attr_text, empty_opt) {
    var cidade = field_cidade.val();
    field_uf.on('change', function(){
        $.get(url, {uf: $(this).val()}, function(data){
            field_cidade.html(populate_combo(data.object_list, attr_value, attr_text, empty_opt)).val(cidade);
        }, 'json');
    });
    field_uf.change();  
}

function populate_combo(items, attr_value, attr_text, empty_opt) {
    var opt = (empty_opt !== null) ? '<option value="">'+empty_opt+'</option>' : '';
    $.each(items, function(i, item){
        opt += '<option value="'+item[attr_value]+'">'+item[attr_text]+'</option>';
    });
    return opt;
}

