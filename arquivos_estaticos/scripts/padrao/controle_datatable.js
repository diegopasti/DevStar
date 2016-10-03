function configurar_datatable_padraok(datatable_id){
	
	$(datatable_id).DataTable({
		responsive: true,
		"bPaginate": false,
		"lengthMenu": [[10, 100, -1], [10, 100, "All"]],
		"dom": '<"top">rt<"clear">',
		"bSort": false,
		"ordering": false,
		"bAutoWidth": false,
		"bFilter": false,
		"aoColumns": [
	        { "sWidth": "null" },
	        { "sWidth": "60px"},  
	        { "sWidth": "60px"},
	        { "sWidth": "60px"},
	        { "sWidth": "60px"}
	        ]
	});

}

/*
function configurar_datatable_selecionavel(datatable,botao_apagar,tem_dados){
	
	var table = $(datatable).DataTable();
	
    $(datatable+' tbody').on( 'click', 'tr', function () {

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
    		desabilitar_botao(botao_apagar);
    	}
    } );
}

*/

function configurar_datatable_selecionavel(datatable,botao_apagar,tem_dados){
	
	var table = $(datatable).DataTable();
	
	tem_dados = parseInt(tem_dados);
	
	 $(datatable+' tbody').on('click', 'tr', function () {
		 
	     if ( $(this).hasClass('selected') ) {
	    	 $(this).removeClass('selected');
	    	 desabilitar_botao(botao_apagar);
	     }
	     else {
	    	 table.$('tr.selected').removeClass('selected');
	    	 $(this).addClass('selected');
	    	 habilitar_botao(botao_apagar);
	     }
		
	 });
	 
    $(botao_apagar).click( function () {
    	
        table.row('.selected').remove().draw( false );
        /*
        if (tem_dados == 1){
        	 alert("Tem que desabilitar a opcao de concluir");
			 desabilitar_botao("#bt_gerar_protocolo");
		 }
		 */
        
    } );
}