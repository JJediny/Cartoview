$(document).ready(function () {
    $('#copyright').css('color', 'white')
     $('#copyright-link').css('color', '#40e0d0');

	$(document).mousemove(function (e) {
	

		TweenLite.to($('body'), .5, {
			css : {
				'background-position' : parseInt(event.pageX / 8) + "px " + parseInt(event.pageY / 12) + "px, " + parseInt(event.pageX / 15) + "px " + parseInt(event.pageY / 15) + "px, " + parseInt(event.pageX / 30) + "px " + parseInt(event.pageY / 30) + "px"
			}
		});
	});
});