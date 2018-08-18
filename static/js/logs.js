currentUsername = document.getElementById("id_username").value;

function getLogs() {
	var xmlHttp = new XMLHttpRequest();

	xmlHttp.onreadystatechange = function() {

		if (xmlHttp.readyState == 4) {

			if(xmlHttp.status == 200) {

				openNewPage(xmlHttp.responseText);
			} else {

				alert(xmlHttp.responseText);
			}
		}
	}

	xmlHttp.open("GET", QUEST_LOGS_URL + currentUsername, true); // true for asynchronous 

	xmlHttp.send();
}

function openNewPage(logs) {

	log_window = window.open("", "Logs", [status=0]);

	var jsonObj = JSON.parse(logs);

	log_collection = jsonObj.logs;

	for (i = 0; i < log_collection.length; i++) { 
		
		// log_window.document.write("<b>Username</b>: " + log_collection[i][0]);
		// log_window.document.write("<br>");
		log_window.document.write("<b>Sentence</b>: " + log_collection[i][1]);
		log_window.document.write("<br>");
		log_window.document.write("<b>Answer</b>: " + log_collection[i][2]);
		log_window.document.write("<br>");
		log_window.document.write("<b>Time</b>: " + log_collection[i][3]);
		log_window.document.write("<br>");
		log_window.document.write("<b>Statistics</b>:<br>" + log_collection[i][4]);
		log_window.document.write("<br>");
		log_window.document.write("<b>Record Time</b>: " + log_collection[i][5]);
		log_window.document.write("<br>--------------------<br>");
	};
}