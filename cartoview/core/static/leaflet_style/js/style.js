window.Cartoview = window.Cartoview || {};
(function ($) {
	Cartoview.LeafletStyler = {
		style:function(style){
			return function(feature){
				return style.style
			}
		},
		pointToLayer:function(style){
			return function(feature, latlng) {
				if(style.style.iconUrl){
		        	return L.marker(latlng, {icon:L.icon(style.style)});
		    	}
		    	else{
		    		return L.circleMarker(latlng, style.style);
		    	}
		    }
		},
		getLeafletStyle: function(style){
			return Cartoview.LeafletStyler[style.featureType][style.type](style);
		},
		point:{
			user_def:function(style){},
			field:function(style){},
			single:function(style){return L.icon(style.style);}
		},
		line:{
			user_def:function(style){},
			field:function(style){},
			single:function(style){}
		},
		polygon:{
			user_def:function(style){},
			field:function(style){},
			single:function(style){}
		}
	}
})(jQuery);
//  L.icon({
//     iconUrl: myURL + 'images/pin24.png',
//     iconRetinaUrl: myURL + 'images/pin48.png',
//     iconSize: [29, 24],
//     iconAnchor: [9, 21],
//     popupAnchor: [0, -14]
// });