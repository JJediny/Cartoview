(function(){
	var header_tpl = "<tr>{#foreach $T as col}<th>{$T.col.title}</th>{#/for}</tr>"
	$.fn.datagrid = function(options) {
		this._datagrid = {
			options:options
		}
	    var head = $("<thead/>").setTemplate(header_tpl).processTemplate(options.columns);
	    $(this).append(head);
	};
	$.fn.appendDataRow = function(data){

	}
})();
/*
How to use
 	html : <table id="table-datagrid" class="table table-bordered table-condensed"></table>
	js: $('#table-features').datagrid({
				data:[{col1:'val1,.....},.....],
				columns:[{name:'col1',title:'Column 1'},....]
			})
*/