var site_rest_url = REST_URL + "core/keyvaluegroup/"
var home_rest_url = site_rest_url;
{% load static %}
// $('#btn-apps').click(function(event) {
// 	event.preventDefault()
// 	$(".app-link").toggleClass('hidden');
// });

$("#btn-install-app").click(function(event) {
	event.preventDefault();
	$('#ct-install-result').empty().append(msg_div('Installing application, Please wait!','info loading'));
	var formData = new FormData($('#form-install-app')[0]);
	//data = {name:'test_install'};
	$.ajax({
        type: 'POST',
        //contentType: 'application/json',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
		url: "{% url 'cartoview2_install_app_url' %}",
        success: function(res, status, jqXHR) {
        	if(res.success){                
                $.each(res.log, function(index, log) {
                     msg_div(log,'info','#ct-install-result');
                });
                $.each(res.warnings, function(index, warning) {
                     msg_div(warning,'warning','#ct-install-result');
                });
                $('#btn-show-install').show();
                $('#ct-install').hide();
                msg_div('Restarting the server, Please wait!','info loading', '#ct-install-result')
                var pleaseWaitDiv = $('<div class="modal" id="pleaseWaitDialog" data-backdrop="static" data-keyboard="false"><div class="modal-body" style="margin: 20% 50%;"><img src="{% static 'images/ajax-loader.gif' %}"/></div></div>');
                pleaseWaitDiv.modal();
                window.setTimeout(function(){get_installed_app_info(res.app_name);}, 5000);
            }
            else{
                $('#ct-install-result').empty()
                $.each(res.errors, function(index, err) {
                     msg_div(err,'danger','#ct-install-result');
                });
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $('#ct-install-result').empty()
            msg_div(jqXHR.responseJSON.error_message,'danger','#ct-install-result');
            msg_div(jqXHR.responseJSON.traceback,'danger','#ct-install-result');    
        },
        xhr: function() {  // Custom XMLHttpRequest
            var myXhr = $.ajaxSettings.xhr();
            if(myXhr.upload){ // Check if upload property exists
                myXhr.upload.addEventListener('progress',progressHandlingFunction, false); // For handling the progress of the upload
            }
            return myXhr;
        }
    }); // end $.ajax()
});
function get_installed_app_info(app_name){
    $.ajax({
        dataType: "json",
        url: REST_URL + "core/app/",
        data:{
            name:app_name,
            format: 'json'
        },
        success:function(res){
        	location.reload(true);
            if(res.error){
                msg_div('************* cannot get app info **********','error','#ct-install-result');
                msg_div(res.error,'error','#ct-install-result');
            }
            else{
                msg_div('App installation success!','success','#ct-install-result');
                var tr =$("<tr>")
                tr.appendTo('#table-apps').setTemplateElement("app-row-template").processTemplate(res.objects[0]);
                var a = $('.btn-uninstall-app',tr);
                a.attr('href', a.attr('href').replace('APP_NAME',res.objects[0].name)).click(uninstall_app);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            setTimeout(function(){
                get_installed_app_info(app_name); 
            },1000);  
        }
    });
}
$('#btn-show-install').click(function(event) {
    $('#btn-show-install').hide()
    $('#ct-install').show()
});
$('#btn-hide-install').click(function(event) {
    $('#btn-show-install').show()
    $('#ct-install').hide()
});
function uninstall_app(event) {
    var row = $(this).parents('tr');
    event.preventDefault();
    if(confirm('Uninstall this app? This action cannot be reversed.')){
        $.ajax({   
            contentType: 'application/json',
            url: $(this).attr('href'),
            processData: false,
            success: function(res, status, jqXHR) {
                if(res.success){
                    $('#ct-install-result').empty().append(msg_div('Uninstallation success!','success'));
                    row.remove()
                }
                else{
                    $('#ct-install-result').empty()
                    $.each(res.errors, function(index, err) {
                         msg_div(err,'danger','#ct-install-result');
                    });
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                msg_div(jqXHR,'danger','#ct-install-result');

            }
        }); // end $.ajax()
    }
}
$(".btn-uninstall-app").click(uninstall_app);

function progressHandlingFunction(e){
    if(e.lengthComputable){
        $('progress').attr({value:e.loaded,max:e.total});
    }
}
$('#file-app').change(function(){
    var file = this.files[0];
    var name = file.name;
    var size = file.size;
    var type = file.type;
    //Your validation
});
function msg_div(msg,cls,ct){
    var html = '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + msg;
    var ct_msg = $('<div>').addClass('alert alert-dismissable alert-' + cls).html(html);
    if(ct) ct_msg.appendTo(ct)
    return ct_msg;
}


