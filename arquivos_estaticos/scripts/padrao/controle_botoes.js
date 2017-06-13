function desabilitar_botao(botao_id){
	$(botao_id).prop("disabled", true);
}

function habilitar_botao(botao_id) {
	$(botao_id).prop("disabled", false);
}


function notify(type,title,description){
  new PNotify({
    title: title,
    text: description,
    //auto_display: false,
    hide: true,
    delay: type=='error' ? 5000 : 2000,
    mouse_reset: false,
    type: type,
    styling: 'bootstrap3' // bootstrap3 , fontawesome
  });
  return (type=='error' ? false : true);
}

function info_notify(title,description){
  return notify("info",title,description);
}

function success_notify(title,description){
  return notify("success",title,description);
}

function error_notify(id,title,description){
  document.getElementById(id).focus();
  return notify("error",title,description);
}

function warning_notify(id,titulo,descricao){
  document.getElementById(id).focus();
  return notify("warning",titulo,descricao);
}