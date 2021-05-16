function getHeaders(){
    return {'csrfmiddlewaretoken': $("form input[type=hidden]").val()};
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function serviceGet(endpoint, callBack, onError){
    $.ajax({
        type: "GET",
        url: endpoint,
        success: callBack,
        error: onError
    });
}

function serviceAjax(typeAjax, endpoint, data, headers, onSuccess, onError, dataType){
    $.ajax({
        type: typeAjax,
        url: endpoint,
        data: JSON.stringify(data),
        dataType: dataType,
        contentType: "application/json",
        success: onSuccess,
        error: onError,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $("form input[type=hidden]").val());
            }
        }
    });
}

function servicePost(endpoint, data, headers, onSuccess, onError, dataType){
    serviceAjax("POST", endpoint, data, headers, onSuccess, onError, dataType)
}

function servicePut(endpoint, data, headers, onSuccess, onError, dataType){
    serviceAjax("PUT", endpoint, data, headers, onSuccess, onError, dataType)
}

function servicePatch(endpoint, data, headers, onSuccess, onError, dataType){
    serviceAjax("PATCH", endpoint, data, headers, onSuccess, onError, dataType)
}

function serviceDelete(endpoint, data, headers, onSuccess, onError, dataType){
    serviceAjax("DELETE", endpoint, data, headers, onSuccess, onError, dataType)
}


function genericCall(endpoint, callBack, onErrorCb){
    function onError(xhr, status, error) {
        console.error("GET Error: ", xhr, status, error);
    }
    
    serviceGet(endpoint, callBack, onErrorCb || onError);
}

function genericPost(endpoint, data, callBack, onErrorCb){
    function onError(xhr, status, error) {
        console.error("POST Error: ", xhr, status, error);
    }
    
    var headers = getHeaders();
    servicePost(endpoint, data, headers, callBack, onErrorCb || onError, 'json');
}

function genericPostHTML(endpoint, data, callBack, onErrorCb){
    function onError(xhr, status, error) {
        swal("Error", xhr.responseText.substring(0, 400), "error");
        console.log(xhr, status, error);
        // Bug of not removing the modal
        $("#spinner").modal('hide')
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();
        $("#spinner").hide();
    }
    
      var headers = getHeaders();
      servicePost(endpoint, data, headers, callBack, onErrorCb || onError, 'html');
}

function genericPut(endpoint, data, callBack, onErrorCb){
    function onError(xhr, status, error) {
        console.error("PUT Error: ", xhr, status, error);
    }
    
    var headers = getHeaders();
    servicePut(endpoint, data, headers, callBack, onErrorCb || onError, 'json');
}

function genericPatch(endpoint, data, callBack, onErrorCb){
    function onError(xhr, status, error) {
        console.error("PATCH Error: ", xhr, status, error);
    }
    
    var headers = getHeaders();
    servicePatch(endpoint, data, headers, callBack, onErrorCb || onError, 'json');
}

function genericDelete(endpoint, callBack, onErrorCb){
    function onError(xhr, status, error) {
        console.error("DELETE Error: ", xhr, status, error);
    }
    
    var headers = getHeaders();
    serviceDelete(endpoint, {}, headers, callBack, onErrorCb || onError, 'json');
}
