var edit_tree_field_id_current = '';

/**
* Активировать редактирование поля.
* Для этого нужно открыть модальное окно и активировать работу с деревом
* для выбранного поля
* @param field_id: css id for hidden input
* @param url ajax url
*/
function edit_tree_field(field_id, url) {
    var modal_window = $('#tree_widget_modal');
    modal_window.modal('show');

    if(field_id != edit_tree_field_id_current) {
        
        edit_tree_field_id_current = field_id;
        var modal_body = $('#tree_widget_modal .modal-body');

        modal_body.jstree({
            plugins : ["themes", "json_data", "ui"],
            themes: {"theme": "classic", "icons": false},
            json_data : { 
                ajax : {
                    url : url,
                    data_type: "json",
                    type: "GET",
                    data : function (n) { 
                        var node_id = n.attr ? n.attr("id") : '';
                        return {'node_id': node_id};
                    }
                }
            }
        }).bind("select_node.jstree", function (event, data) {

                var selected_obj = data.rslt.obj

                $("#" + field_id).val(selected_obj.attr("id"));

                var selected_text = '';
                $.each(selected_obj.parents('li').toArray().reverse(), function (i, node) {
                    selected_text += $(node).attr("title") + ' / ';
                });
                selected_text += selected_obj.attr("title");

                $("#" + field_id + "_title").html(selected_text);

                modal_window.modal('hide');
            }
        );

    }
}

/**
 * Очистка иерархического поля при нажатии на remove
 * @param p_input_id
 */
function tree_field_clear(input_id) {
    $('#' + input_id).val('');
    $('#' + input_id + '_title').html('Не выбрано');
}