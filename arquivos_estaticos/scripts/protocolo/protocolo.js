function configurar_pagina(documento){
	var destinatario = document.getElementById('entidade_destinatario');
	if (destinatario.value == "") {
		desabilitar_botao("#bt_novo_documento");
		desabilitar_botao("#bt_apagar");
		desabilitar_botao("#bt_gerar_protocolo");
	} 

	else {
		desabilitar_botao("#bt_apagar");
		habilitar_botao("#bt_novo_documento");
	} 
	
	var class_bt_concluir = $("#bt_gerar_protocolo").attr('class');
	var liberado = class_bt_concluir.search("liberado"); 
	if (liberado == -1){
		desabilitar_botao($("#bt_gerar_protocolo"));
	}
}

function verifica_alteracao_campo(document,campo,botao_documento,botao_concluir){
	//alert("estou vindo no script protocolo configurar o datatable??");
	var class_bt_concluir = $(botao_concluir).attr('class');
	var liberado = class_bt_concluir.search("liberado"); 
	
	
	var destinatario = document.getElementById(campo);
	if (destinatario.value == "") {
		desabilitar_botao(botao_documento);
		desabilitar_botao(botao_concluir);
		
	} else {
		
		habilitar_botao(botao_documento);

		if (liberado == -1){
			desabilitar_botao(botao_concluir);
		}
		else{
			habilitar_botao(botao_concluir);
		}		
	} 
}

function configurar_datatable_selecionavel(datatable,botao_apagar,tem_dados){
	
	var table = $(datatable).DataTable();
	
    $(datatable+' tbody').on( 'click', 'tr', function () {
    	
    	//habilitar_botao(botao_apagar);
    	//alert("Vim aqui no configurar_datatable ou nao?");
    	if (tem_dados){
    		//alert("Tem dados armazenados ainda");
    		if ($(this).hasClass('selected') ) {
                $(this).removeClass('selected');
                desabilitar_botao(botao_apagar);
            }
            else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
                habilitar_botao(botao_apagar);
            }
    	}
    	
    	else{
    		//alert("tem dados sim nos dados");
    		desabilitar_botao(botao_apagar);
    		desabilitar_botao("#bt_gerar_protocolo");
    	}
    } );
}


function configurar_datatable(datatable_id){
	
	//alert("eh esse datatable aqui");
	$(datatable_id).DataTable({
		'responsive': true,
		"bPaginate": false,
		"lengthMenu": [[10, 100, -1], [10, 100, "All"]],
		"dom": '<"top">rt"<"rightcolumn"p><"clear">',
		"bSort": false,
		"ordering": false,
		"bAutoWidth": false,
		"bFilter": false,
		"aoColumns": [
	        { "sWidth": null },
	        { "sWidth": "100px" },
	        { "sWidth": "100px" },  
	        { "sWidth": "120px"}
	        ]
	
	
	});
}