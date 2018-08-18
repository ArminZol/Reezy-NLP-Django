$('html').click(function(e) {
	if (!$(e.target).hasClass('slider-text'))
	{
		if ($(e.target).hasClass('left-right')) {
			$('.slider').css('visibility', 'visible');
			$('.slider').stop().animate({
				left: '80%'
			}, 400, function() {
				$('.simplification_button').css('visibility', 'hidden')
			});
		}
		else
		{
			$('.simplification_button').css('visibility', 'visible')
			$('.slider').stop().animate({
				left: '100%'
			}, 400, function() {
				$(this).css('visibility', 'hidden')
			});
		}
	}
});