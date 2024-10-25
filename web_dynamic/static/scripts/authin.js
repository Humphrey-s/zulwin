$(document).ready(function () {

	$(".continue-btn").click(function () {
		let name = $("#input-name").val();
		let email = $("#input-email").val();
		let pwd = $("#input-pwd").val();

		let dct = {"name": name, "email": email, "password": pwd}
		console.log(dct);
		$.ajax({
			type: "POST",
			url: "/resource/s/aOuth?{{cache_id}}",
			data: dct,
			success: function (data) {
				console.log("aOuth")
				window.location.replace(`/auth/OTP?${data.id}`);
			}
		})
	});

	$("#signup-form").on('submit', function (event) {
		event.preventDefault();

		var form_data = new formData(this);
		console.log("hallo2");

		$.ajax({
			type: "POST",
			url: "/resource/s/aOuth?{{cache_id}}",
			data: form_data,
			success: function (data) {
				console.log("aOuth")
				$("#url_for_otp").click();
			}
		});
	});
})