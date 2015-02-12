function load_apps(url){
    $.ajax({
        dataType: "json",
        url: url,
        success:function(data){
            $("#ct-apps-list").setTemplateElement("apps-list-template").processTemplate(data);
            $('#btn-previous,#btn-next').click(function(e){
                e.preventDefault();
                load_apps($(this).attr('href'));
            })
        }
    });
}
$(function(){
    $("#menu-toggle").click(function(e) { e.preventDefault(); $("#wrapper").toggleClass("active"); });
    //load list of apps
    load_apps(REST_URL + 'core/app/?format=json&limit='+ ITEMS_PER_PAGE)
    //load the applications list into the drop-down list for add new instance
    //$("#apps-dd-list").setTemplateElement("apps-dd-template").processTemplateURL(REST_URL + 'core/app/?format=json');
   
});