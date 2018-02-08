$(document).ready(function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    $("#form").submit(function(event){
        event.preventDefault();
        $.ajax({
            url: "/payments/ajax/check_reg_form/",
            data: {
                'email': $("#id_email").val(),
                'pas': $("#id_pas").val(),
                'ver_pas': $("#id_ver_pas").val(),
                'conv': $("#id_conv").val()
            },
            type: "POST",
            dataType: 'json',
            success: function(data){
                if(data.success){
                    window.location.replace(data.redirect_page);
                }
                else{
                    $("#id_error").text(data.error);
                    $("#id_error").effect("shake");
                }
            }
        });
    });

    $("#check_form").click(function(event) {
        if($("#id_conv").prop('checked') == "checked"){
            $('#form').submit();
        } else {
            $("#form").effect("shake");
        } 
    });
});
