// using jQuery
function getCookie(name) {

	var cookieValue = null;

	if (document.cookie && document.cookie !== "") {
		var cookies = document.cookie.split(";");

		for (var i = 0; i < cookies.length; i++) {

			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + "=")) {
				
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	
	return cookieValue;
}

function post(url, params, success, error) {

	params.csrfmiddlewaretoken = getCookie("csrftoken");

	$.ajax({

		type: POST,
		url: url,
		data: params,

		success: function() {

			Materialize.toast(success, 4000);
		},

		error: function() {

			Materialize.toast(error, 4000);
		}
	});
}

function silent_post(url, params) {

	params.csrfmiddlewaretoken = getCookie("csrftoken");

	$.ajax({
		type: POST,
		url: url,
		data: params
	});
}