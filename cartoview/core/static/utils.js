window.cartoview2 = window.cartoview2 || {};
cartoview2.utils = (function(){
	var ids_counter = {};
	var get_id = function(prefix){
		prefix = prefix || 'id_';
		if(ids_counter[prefix] == undefined) ids_counter[prefix] = 0;
		return prefix + '' + ids_counter[prefix]++;
	};
	return {
		get_id : get_id,
		form_to_json:function(form){
			var $f = $(form);
		    var o = {};
		    var a = $f.serializeArray();
		    $.each(a, function() {
		        if (o[this.name] !== undefined) {
		            o[this.name] += "," + (this.value || '');
		        } else {
		            o[this.name] = this.value || '';
		        }
		    });
		    return o;
		},
		submit_rest_form:function(options) {
			var data = options.data ;
			if(!data){
				data = form2js(options.form_id);
			} 
			$.ajax({
	            type: options.method || 'POST',
	            contentType: 'application/json',
	            data: JSON.stringify(data),
	            dataType: 'json',
	            processData: false,
	            url: options.url,
	            success: function(data, status, jqXHR) {
	            	//alert('success');
	            },
	            error: function(jqXHR, textStatus, errorThrown) {
	            	console.log(jqXHR);   
	            }
	        }); // end $.ajax()
		},
		ui:{
			loading:function(msg,ct){
				
			},
			form_defaults:{
				one_line_input:true,
				label_cls:'col-sm-2',
				input_cls:'col-sm-8'
			},
			form:function(ct){
				var id = get_id('form');
				return $('<form />').addClass('form-horizontal').attr('role',"form" ).attr('id', id).appendTo(ct);
			},
			input_wrapper:function(ct,label,input_id){
				var div = $('<div class="form-group" />').appendTo(ct);
				var $label = $('<label class="control-label" />').text(label).attr('for',input_id).appendTo(div);
				var $wrapper = $('<div />').appendTo(div);
				
				if(cartoview2.utils.ui.form_defaults.one_line_input){
					$label.addClass(cartoview2.utils.ui.form_defaults.label_cls);
					$wrapper.addClass(cartoview2.utils.ui.form_defaults.input_cls);
				}
				return $wrapper;
			},
			input:function(ct,name,label,no_wrap){
				var id = get_id('input');
				var $input = $('<input>').attr('id',id).attr('name',name).addClass('form-control');
				if(no_wrap){
					$input.appendTo(ct);
				}
				else{
					var wrapper = cartoview2.utils.ui.input_wrapper(ct,label,id);
					$input.appendTo(wrapper);
				}
				return $input;
			},
			textbox:function(ct,name,label,placeholder,value,no_wrap){
				
				var $input = cartoview2.utils.ui.input(ct,name,label,no_wrap);
				$input.attr('placeholder',placeholder).attr('type','text').val(value);
				return $input;
			},
			textarea:function(ct,name,label,placeholder,value,no_wrap){
				var id = cartoview2.utils.get_id();
				var $input = $('<textarea>').attr('id',id).attr('name',name).attr('placeholder',placeholder).addClass('form-control').val(value);
				if(no_wrap){
					$input.appendTo(ct);
				}
				else{
					var wrapper = cartoview2.utils.ui.input_wrapper(ct,label,id);
					$input.appendTo(wrapper);
				}
				return $input;
			},
			hidden_field:function(ct,name,value){
				var id = get_id('input');
				var $input = $('<input>').attr('type','hidden').attr('id',id).attr('name',name).val(value).appendTo(ct);
				return $input;
			},
			checkbox:function(ct,name,value,label,checked,no_wrap){
				var $input = cartoview2.utils.ui.input(ct,name,label,no_wrap);
				$input.attr('type','checkbox').val(value);
				if(checked){
					$input.attr('checked', 'checked');
				}
				return $input;
			},
			checkbox_group:function(ct,name,label,values,no_wrap,item_add_callback,scope){
				var $wrapper;
				if(no_wrap){
					$wrapper = $(ct);
				}
				else{
					$wrapper = cartoview2.utils.ui.input_wrapper(ct,label,name);
				}
				$.each(values,function(key,text){
					var $ct = $('<div/>').addClass('checkbox').appendTo($wrapper)
					$input = cartoview2.utils.ui.checkbox($ct, 'basemaps', key, text, false, true).removeClass('form-control');
					var $label = $('<label/>').text(text).appendTo($ct);
					$label.attr('for',$input.attr('id'));
					$input.appendTo($label)
					if(typeof item_add_callback == 'function'){
						item_add_callback.call(scope || $wrapper, key, text, $input, $ct, $label);
					}
				});
				return $wrapper;
			},
			radiobox:function(ct,name,value,label,checked,no_wrap){
				var $input = cartoview2.utils.ui.input(ct,name,label,no_wrap);
				$input.attr('type','radio').val(value);
				if(checked){
					$input.attr('checked', 'checked');
				}
				return $input;
			},
			button:function(ct,text,cls,handler,scope){
				var $btn = $('<input/>').val(text).attr('type','button').addClass('btn').addClass(cls).appendTo(ct);
				if(typeof handler == 'function') {
					$btn.click(function(e){
						e.preventDefault();
						handler.call(scope||this,e);
					})
				}
				return $btn;
			},
			submit:function(ct,text,cls,handler,scope){
				var $btn = $('<button/>').text(text).attr('type','submit').addClass('btn').addClass(cls).appendTo(ct);
				if(typeof handler == 'function') {
					$btn.click(function(e){
						e.preventDefault();
						handler.call(scope||this,e);
					})
				}
				return $btn;
			},
			link_button:function(ct,text,cls,handler,scope){
				var $btn = $('<a/>').text(text).attr('href','#').addClass('btn').addClass(cls).appendTo(ct);
				if(typeof handler == 'function') {
					$btn.click(function(e){
						e.preventDefault();
						handler.call(scope||this,e);
					})
				}
				return $btn;
			},
			dropdown:function(ct,name,label,values,selected_val,no_wrap){
				var id = cartoview2.utils.get_id();
				var $input = $('<select>').attr('id',id).attr('name',name).addClass('form-control');
				$.each(values, function(key, text) {
					 $('<option/>').attr('value', key).text(text).appendTo($input)
				});
				$input.val(selected_val);
				if(no_wrap){
					$input.appendTo(ct);
				}
				else{
					var wrapper = cartoview2.utils.ui.input_wrapper(ct,label,id);
					$input.appendTo(wrapper);
				}
				return $input;
			},
			tabs:function(ct, titles, active_tab,horizintal){
				active_tab = active_tab || 0;
				
				var tabs = {
					addTab:function(title){
						var id = cartoview2.utils.get_id();
						var $btn = $('<a />').attr('href','#'+id).addClass('list-group-item').text(title).appendTo(tabs.header);
						$btn.click(function(e){
							e.preventDefault();
							$('div.card-ct',tabs.content).hide();
							$('a',tabs.header).removeClass('active');
							$(this).addClass('active')
							$($(this).attr('href')).show();
						});
						
						var $tab = $('<div />').attr('id',id).addClass('card-ct').appendTo(tabs.content).hide();
						tabs.containers.push($tab);
						if(tabs.containers.length - 1 == active_tab){
							$btn.addClass('active');
							$tab.show();
						}
						return $tab;
					},
					containers:[]
				}
				if(horizintal){
					//TODO:
				}
				else{
					var $header = $('<div />').addClass('col-md-3').appendTo(ct);
					tabs.header = $('<div />').addClass('list-group').appendTo($header);
					tabs.content = $('<div />').addClass('col-md-9').appendTo(ct);
					$.each(titles,function(index,title){
						tabs.addTab(title);
					})
				}
				
				return tabs;
			}
		}
	}
})()
