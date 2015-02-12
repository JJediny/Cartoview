$(document).ready(function() {
    $('.autocomplete_widget').each(function() {
        bind_autocomplete_widget(this);
    });
});

function bind_autocomplete_widget(element) {
    
    var j_element = $(element);
    var url = j_element.attr('data-url');
    var expression = j_element.attr('data-expression');
    var where = j_element.attr('data-where');
    var where_params = j_element.attr('data-where_params');

    $(element).select2({
        placeholder: "Поиск элемента",
        minimumInputLength: 3,
        multiple:false,
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
                    data: {q: id, expression: 'id', where: where, where_params: where_params},
                    dataType: "json"
                }).done(function(data) { 
                    callback(data[0]); 
                });
            }
        },
        dropdownCssClass: "bigdrop", // apply css that makes the dropdown taller
        escapeMarkup: function (m) { return m; } // we do not want to escape markup since we are displaying html in results
    });

}