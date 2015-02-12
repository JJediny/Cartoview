$(document).ready(function() {
    $('.autocomplete_multiple_widget').each(function() {
        bind_autocomplete_multiple_widget(this);
    });
});

function bind_autocomplete_multiple_widget(element) {
    
    var j_element = $(element);
    url = j_element.attr('data-url');
    var expression = j_element.attr('data-expression');
    var where = j_element.attr('data-where');
    var where_params = j_element.attr('data-where_params');

    $(element).select2({
        placeholder: "Enter User name",
        minimumInputLength: 1,
        multiple: true,
        ajax: {
            url: url,
            quietMillis: 1000,
            dataType: 'json',
            data: function (term, page) { return {q: term, expression: expression, where: where, where_params: where_params}; },
            results: function (data, page) {
                return {results: data};
            }
        },
        initSelection: function(element, callback) {
            var id = $(element).val();
            if (id !== "") {
                $.ajax(url, {
                    data: {q: id, expression: 'pk__in', where: where, where_params: where_params},
                    dataType: "json"
                }).done(function(data) { 
                    callback(data); 
                });
            }
        },
        dropdownCssClass: "bigdrop",
        escapeMarkup: function (m) { return m; }
    });

}