/*
 * Globais
 ******************************************************************************/
var tipo_locomocao = $('#id_tipo_locomocao');
var cod_tipo_locomocao = tipo_locomocao.val();

/*
 * Máscaras
 ******************************************************************************/
if ($('.mask-moeda').length || $('.mask-data').length) {
	$('.mask-data').mask(mascaras.data);
	$('.mask-moeda').priceFormat(cfgPriceFormat);
}

$('.calendario_ui').datepicker(cfgCalendario);

/*
 * Bloqueia itens no 'form' por tipo de locomoção
 ******************************************************************************/
combustivel();

tipo_locomocao.on('change', function() {
	tipo_locomocao.closest('form').find("input[type=text], textarea").val('');
	cod_tipo_locomocao = tipo_locomocao.val();
	combustivel();
});

function combustivel() {
	if (cod_tipo_locomocao !== 'combustivel') {
		$('#id_combustivel').val('');
		$('#id_combustivel').attr('disabled', true);
	} else {
		$('#id_combustivel').attr('disabled', false);
	}
}

/*
 * Mostra tela de alterção
 ******************************************************************************/
$('#tb-locomocao-consulta > tbody > tr td:not(.down)').on('click', function(){
	location.href = $(this).parent().attr('url-edit');
});

$('.no-action').on('click', function(){
	location.href = '/locomocao/consulta';
});

/*
 * Informar comprovante não entregue
 ******************************************************************************/
 $('.down').on('click', function(){
 	var url = $(this).parent().attr('url-sem-comprovante');
 	var entregador_nome = $(this).parent().find('.entregador_nome').text();
 	$('#confirm .modal-body').html('<p>Você tem certeza que deseja salvar comprovante não entregue para <strong>'+entregador_nome+'</strong> ?</p>');
 	$('#bt-confirm').attr('href', url);
 	$('#confirm').modal('show');
 });