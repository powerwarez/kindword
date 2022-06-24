//modal//
/*https://codepen.io/jaehee/pen/BpXjLx*/

var $button         = $('.button'),
    $modalContainer = $('#modal-container'),
    $body           = $('body'),
    $content        = $('.content'),
	$usernameTag    = $('.usernameShow'),
    btnId;

$button.on('click', function () {
	btnId = $(this).attr('id');
	
	$modalContainer
			.removeAttr('class')
			.addClass(btnId);
	$content
			.removeAttr('class')
			.addClass('content');
	
	$body.addClass('modal-active');

	$content.addClass(btnId);

	$usernameTag
			.removeAttr('usernameShow')
			.addClass('usernameHide');
	
});