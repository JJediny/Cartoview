(function ($) {

var MARKERS_ROOT = STATIC_URL + "markers/"
DEFAULT_MARKER_STYLE = {
	type:'single',
	featureType:'point',
	style:MARKERS_LIST[0],
	focus_style:MARKERS_LIST[0]
};
var DEFAULT_POLYGON_STYLE = {
	'color':"#000000",
	'weight':1,
	'opacity':1,
	'dashArray':"",
	"fillColor":"#FFFFFF",
	"fillOpacity":1
};
var DEFAULT_LINE_STYLE = DEFAULT_POLYGON_STYLE;
var id_counter =  0;
function new_id(){
	return "styler-" + (id_counter++);
}
var stylersDict = {};
function getStyleFromValue(input){
	var value = input.val()
	if(value && value != ""){
		try{
			return JSON.parse(value);
		}
		catch(err){
			return null;
		}
	}
	return null;
}
$.fn.markerChooser = function(){

	var input = this;
	if(!this.chooser){
		var ct  = this.chooser = $('<div class="dropdown icon-picker">').insertAfter(input);
		
	    input.hide()
	    var btn = $('<button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown">');
	    btn.appendTo(ct).attr('id',input.attr('id')+ "-btn");

	    var img = $("<img>").appendTo(btn);
	    var value = input.val();
	    var style = (value && value != "") ? JSON.parse(value) : MARKERS_LIST[0];
	  
	    btn.append('<span class="caret"></span>');
	    
    	img.attr("src", style.iconUrl);
	    var ul = $('<ul class="dropdown-menu" role="menu">').appendTo(ct).attr("aria-labelledby",btn.attr("id"));
	    
	    $.each(MARKERS_LIST,function(index, marker){
	        var li = $('<li>') .appendTo(ul);
	        if(style == marker) li.addClass("active")
	        var img_btn = $('<a role="menuitem" tabindex="-1" href="#">').appendTo(li)
	        var img_url =  marker.iconUrl;

	        $("<img>").attr("src", img_url).appendTo(img_btn);
	        img_btn.click(function(e){
	            e.preventDefault();
	            img.attr("src", marker.iconUrl);
	            $('li', ul).removeClass('active');
	            li.addClass('active');
	            input.val(JSON.stringify(marker)); 
	            input.trigger('marker-change');
	        });
	    });

	}
	return input;
}

/////////////////////////////
///////////////////////////////
$.fn.leafletStyler = function(options){
	options = options || {};
	var input = $(this);
	var stylerId = input.attr("styler-id")
	if(!stylerId){
		var tpl = $('#styler_html').html();
		Mustache.parse(tpl);   // optional, speeds up future uses
		var prefix = new_id();
		var style = options.style || getStyleFromValue(input) || DEFAULT_MARKER_STYLE;
		console.debug(style)
		var context = {
			prefix:prefix,
			is_point: style.featureType == 'point',
			is_line: style.featureType == 'line',
			is_polygon: style.featureType == 'polygon'
		}
		console.debug(context)
		var rendered = $(Mustache.render(tpl, context)).insertAfter(input);
		var pointOptions = {
			appendTo : $("#" + prefix + "-point-styler-ct",rendered)
		}
		if(context.is_point) pointOptions.style = style;
		input.leafletPointStyler(pointOptions);
		
		var lineOptions = {
			appendTo : $("#" + prefix + "-line-styler-ct",rendered)
		}
		if(context.is_line) lineOptions.style = style;
		input.leafletLineStyler(lineOptions);

		var polygonOptions = {
			appendTo : $("#" + prefix + "-polygon-styler-ct",rendered)
		}
		if(context.is_polygon) polygonOptions.style = style;
		input.leafletPolygonStyler(polygonOptions);


		stylerId = $(".tab-pane.active",rendered).find("div.styler").attr("styler-id");
		input.attr("styler-id",stylerId);
		
		$("select[name='featureType']",rendered).change(function(){
			var tab = $($(this).val());
			$(".styler-tab.active", rendered).removeClass("active");
			tab.addClass('active');
			stylerId = tab.find("div.styler").attr("styler-id");
			input.attr("styler-id",stylerId);

		})
	}
	return input;
}
/////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////// POINT STYLER /////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
$.fn.leafletPointStyler = function(options){
	options = options || {};

	var input = $(this);
	var stylerId = input.attr("point-styler-id")
	if(!stylerId){
		var tpl = $('#point_styler_html').html();
		Mustache.parse(tpl);   // optional, speeds up future uses

		stylerId = new_id();
		input.attr("point-styler-id", stylerId);
		var style = options.style || getStyleFromValue(input) || DEFAULT_MARKER_STYLE;

		
		var rendered = $(Mustache.render(tpl, {
			prefix: stylerId,
			is_single: style.type == "single",
			is_user_def: style.type == "user_def",
			is_field: style.type == "field"
		}));

		

		if(options.appendTo) {
			rendered.appendTo(options.appendTo);
		}
		else {
			rendered.insertAfter(this);
		}
		this.hide()
		$("select[name='type']",rendered).change(function(){
			$(".tab-pane.active", rendered).removeClass("active");
			$($(this).val()).addClass('active');
		})
		
		$("input[name='style']", rendered).val(JSON.stringify(style.style)).markerChooser();
		$("input[name='focus_style']", rendered).val(JSON.stringify(style.focus_style)).markerChooser();

		stylersDict[stylerId] = { 
			getLeafletStyle : function(){
				var activeStyler = $(".tab-pane.active", rendered);
				var style =  {
					type: activeStyler.attr("style-type"),
		    		featureType:'point',
		    		style: JSON.parse($("input[name='style']",activeStyler).val()),
		    		focus_style: JSON.parse($("input[name='focus_style']",activeStyler).val())
				}
				return style;
			}
		}
	}
	return this;
}
//////////////////////////////////////////////////////////////////////////////////////
///////////////////////////// LINE STYLER ////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////
$.fn.leafletLineStyler = function(options){
	options = options || {};
	var input = $(this);
	var stylerId = input.attr("line-styler-id");
	if(!stylerId){
		var tpl = $('#line_styler_html').html();
		Mustache.parse(tpl);   // optional, speeds up future uses

		stylerId = new_id();
		input.attr("line-styler-id", stylerId);
		var style = options.style || getStyleFromValue(input) || {
    		type:'single',
    		featureType:'line',
    		style: DEFAULT_LINE_STYLE
    	};
	    
		var rendered = $(Mustache.render(tpl, {
			prefix: stylerId,
			is_single: style.type == "single",
			is_user_def: style.type == "user_def",
			is_field: style.type == "field",
			dasharrays:  ["","5, 5", "5, 10", "10, 5","5, 1", "1, 5", "0.9", "15, 10, 5", "15, 10, 5, 10", "15, 10, 5, 10, 15", "5, 5, 1, 5"]
		}));

		if(options.appendTo) {
			rendered.appendTo(options.appendTo);
		}
		else {
			rendered.insertAfter(this);
		}
		this.hide()
		// var updateStyle = function(){
		// 	input.updateStyle()
		// }
		$("select[name='type']",rendered).change(function(){
			$(".tab-pane.active", rendered).removeClass("active");
			$($(this).val()).addClass('active');
		})
		$("input[name='color']", rendered).attr("defaultColor",style.style["color"]).simpleColor();
		$("input[name='opacity']", rendered).val(style.style["opacity"]);
		$("input[name='weight']", rendered).val(style.style["weight"]);
		$("[dasharray='"+ style.style["dashArray"] +"']", rendered).addClass('active');
		$(".svg-dasharray", rendered).find('a').click(function(e){
			e.preventDefault();
			$(this).parents(".svg-dasharray").find("div").removeClass('active')
			$(this).parent().addClass("active");
		});
		stylersDict[stylerId] = {
			getLeafletStyle: function(){
				var style =  {
					type:'single',
		    		featureType:'line',
		    		style:{
		    			'color': $("input[name='color']", rendered).val(),
		    			'weight': $("input[name='weight']", rendered).val(),
		    			'opacity':$("input[name='opacity']", rendered).val(),
		    			'dashArray':$(".svg-dasharray", rendered).find('div.active').attr("dasharray")
		    		}
				}
				return style;

			}
		}
	}
	return $(this);
}
//////////////////////////////////////////////////////////////////////////////////////
///////////////////////////// POLYGON STYLER ////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////
$.fn.leafletPolygonStyler = function(options){
	options = options || {};
	var input = $(this);
	var stylerId = input.attr("polygon-styler-id");
	if(!stylerId){
		var tpl = $('#polygon_styler_html').html();
		Mustache.parse(tpl);   // optional, speeds up future uses

		stylerId = new_id();
		input.attr("polygon-styler-id", stylerId);
		var style;
		var style = options.style || getStyleFromValue(input) || {
    		type:'single',
    		featureType:'polygon',
    		style:DEFAULT_POLYGON_STYLE
    	};
	    
		var rendered = $(Mustache.render(tpl, {
			prefix: stylerId,
			is_single: style.type == "single",
			is_user_def: style.type == "user_def",
			is_field: style.type == "field",
			dasharrays:  ["","5, 5", "5, 10", "10, 5","5, 1", "1, 5", "0.9", "15, 10, 5", "15, 10, 5, 10", "15, 10, 5, 10, 15", "5, 5, 1, 5"]
		}));

		if(options.appendTo) {
			rendered.appendTo(options.appendTo);
		}
		else {
			rendered.insertAfter(this);
		}
		this.hide()
		$("select[name='type']",rendered).change(function(){
			$(".tab-pane.active", rendered).removeClass("active");
			$($(this).val()).addClass('active');
		});
		$("input[name='color']", rendered).attr("defaultColor",style.style["color"]).simpleColor();
		$("input[name='fillColor']", rendered).attr("defaultColor",style.style["fillColor"]).simpleColor();
		$("input[name='opacity']", rendered).val(style.style["opacity"]);
		$("input[name='fillOpacity']", rendered).val(style.style["fillOpacity"]);
		$("input[name='weight']", rendered).val(style.style["weight"]);
		$("[dasharray='"+ style.style["dashArray"] +"']", rendered).addClass('active');
		$(".svg-dasharray", rendered).find('a').click(function(e){
			e.preventDefault();
			$(this).parents(".svg-dasharray").find("div").removeClass('active')
			$(this).parent().addClass("active");
		});
		stylersDict[stylerId] = {
			getLeafletStyle: function(){
				var style =  {
					type:'single',
		    		featureType:'polygon',
		    		style:{
		    			'fillColor': $("input[name='fillColor']", rendered).val(),
		    			'fillOpacity':$("input[name='fillOpacity']", rendered).val(),
		    			'color': $("input[name='color']", rendered).val(),
		    			'weight': $("input[name='weight']", rendered).val(),
		    			'opacity':$("input[name='opacity']", rendered).val(),
		    			'dashArray':$(".svg-dasharray", rendered).find('div.active').attr("dasharray")
		    		}
				}
				return style;

			}
		}
	}
	return $(this);
}
////////////////////////////////////////////////////////////////////////////
//////////////////////////////
////////////////////////////////////////////////////////////////////////////
$.fn.getLeafletStyle = function(){
	var stylerId = $(this).attr("styler-id")
	if(stylerId){
		return stylersDict[stylerId].getLeafletStyle();
		// try{
		// 	var style = {};	
		// 	var activeTab = $(".tab-content .active", styler);
		// 	style.type = activeTab.attr("style-type");
		// 	style.featureType = styler.attr("style-feature-type");
		// 	style.style =  JSON.parse($("[name='style']",activeTab).val());
		// 	style.focus_style = JSON.parse($("[name='focus_style']",activeTab).val());
		// 	this.val(JSON.stringify(style));
		// 	console.debug(this.val())
		// }
		// catch(err){}
	}
	return null;
}

// var originalVal = $.fn.val;
// $.fn.val = function(value) {
// 	console.debug(value)
// 	if(this.styler){
// 		debugger
// 		if (typeof value != 'undefined') {
// 		  // setter invoked, do processing
// 		  return originalVal.call(this, value);
// 		}
// 		//getter
// 		var style = {};
// 		var activeTab = $(".tab-content .active",this.styler);
// 		style.style =  JSON.parse($("[name='style']").val());
// 		style.focus_style = JSON.parse($("[name='focus_style']").val());
// 		originalVal.call(this, JSON.stringify(style));
// 		return originalVal.call(this);
// 	}
// 	return originalVal.call(this, value);
// };

})(jQuery);