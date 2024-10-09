
$(document).ready(function () {


	$(".signin-container").mouseleave(function () {

		$(".signin-container").css("display", "none");
		
		setTimeout(function () {
			$(".header-accounts").css("border", "0");
		}, 100);
	});

	$(".signin-container").mouseover(function () {
		$(".header-accounts").css("border", "0");
	});

	$(".header-accounts").mouseover(function () {
		$(".header-accounts").css("border", "1px solid orange");
		
		setTimeout(function () {
			$(".signin-container").css("display", "flex");
		}, 500);
	})
});