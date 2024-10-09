/*$(document).ready(function () {

	$(".continue-btn").click(function () {
		console.log("Halloo");
	});

	$("#signup-form").on('submit', function (event) {
		event.preventDefault();

		var form_data = new formData(this);

		$.ajax({
			type: "POST",
			url: "/resource/s/aOuth?{{cache_id}}",
			data: form_data,
			success: function (data) {
				console.log("aOuth")
				$("#url_for_otp").click();
			}
			error: function (jqXHR, exception) {
				console.log(jqXHR.status);
			}
		});
	});
})*/