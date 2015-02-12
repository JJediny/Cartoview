var current_url = ''
function load_app_instances(url){
    current_url = url;
    $.ajax({
        dataType: "json",
        url: url,
        success:function(data){
            $("#ct-app-instances-list").setTemplateElement("app-instances-list-template").processTemplate(data);
            $('.panel-body').mouseout(function(event){
                $(this).removeClass('panel-body-active')
            });
            
            $('.panel-image').mouseover(function(event) {
                $(this).next('.panel-body').addClass('panel-body-active')
            });

            $('#btn-previous,#btn-next').click(function(e){
                e.preventDefault();
                load_app_instances($(this).attr('href'));
            })
            $('.delete-instance').click(function(event) {
                event.preventDefault();
                if(confirm("Are you sure you want to delete this?")){
                    var id = $(this).attr('href');
                    $.ajax({
                        dataType: "json",
                        method:'DELETE',
                        url: REST_URL + 'core/appinstance/' + id + '/',
                        success:function(data){
                            load_app_instances(current_url);
                        }
                    });
                }
                return false;
            });
        }
    });
}
$(function(){
    $("#menu-toggle").click(function(e) { e.preventDefault(); $("#wrapper").toggleClass("active"); });
    //load list of app instances
    load_app_instances(REST_URL + 'core/appinstance/?format=json&limit='+ITEMS_PER_PAGE)
    //load the applications list into the drop-down list for add new instance
    //$("#apps-dd-list").setTemplateElement("apps-dd-template").processTemplateURL(REST_URL + 'core/app/?format=json');
   
});