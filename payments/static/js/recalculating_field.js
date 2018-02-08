$(document).ready(function() {

    $.ajax({
        url: "/payments/ajax/get_curse/",
        type: "GET",
        dataType: 'json',
        success: function(data){
            if(data.success !== 0){
                var json = JSON.parse(JSON.stringify(data))['curse'];
                localStorage.setItem('curse', JSON.stringify(json));
            }
            else{
                alert(data.error);
            }
        }
    });

    var json = JSON.parse(localStorage.getItem('curse'));
    var calc_lain = 0;

    $('#id_lain').change(function(){
        var deposit = document.getElementById('id_deposit');
        var summary_depos = document.getElementById('id_summary_depos');
        var max_lain = document.getElementById('id_max_lain');
        val = json[deposit.value+'/'+$(this).val()]*summary_depos.value;
        if (val){
            max_lain.value = Math.round(val);
        }
    });
    $('#id_deposit').change(function(){
        var summary_depos = document.getElementById('id_summary_depos');
        var lain = document.getElementById('id_lain');
        var max_lain = document.getElementById('id_max_lain');
        val = json[$(this).val()+'/'+lain.value]*summary_depos.value;
        if (val){
            max_lain.value = Math.round(val);
        }
    });
    $('#id_summary_depos').change(function(){
        var deposit = document.getElementById('id_deposit');
        var lain = document.getElementById('id_lain');
        var max_lain = document.getElementById('id_max_lain');
        val = json[deposit.value+'/'+lain.value]*$(this).val();
        if (val){
            max_lain.value = Math.round(val);
        }
    });
    $('#id_max_lain').bind('focus', function(event){
        var max_lain = document.getElementById('id_max_lain');
        calc_lain = max_lain.value;
    });

    $('#id_max_lain').bind('change', function(event){
        var max_lain = document.getElementById('id_max_lain');
        max_lain.value = calc_lain;
    });

    $('#id_max_lain').bind('focusout', function(event){
        var max_lain = document.getElementById('id_max_lain');
        max_lain.value = calc_lain;
    });
});


