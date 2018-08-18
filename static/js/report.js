function report() {

	var text = document.getElementById("text");
	var result = last_text;
	var stats = document.getElementById("statistics");

	if(text.value === null || text.value == "") {

		return;
	}

	var params = {
		text: text.value,
		result: result,
		stats: stats.innerHTML
	};

	post(SIMP_URL, params, "Thanks! Report sent", "Error sending report");
}