function getGlobalWord() {

	var xmlHttp = new XMLHttpRequest();

	xmlHttp.onreadystatechange = function() {

		if (xmlHttp.readyState == 4) {

			if(xmlHttp.status == 200) {
			
				extractGlobalWord(xmlHttp.responseText);
			} else {

				extractGlobalWord(null);
			}
		}
	}

	xmlHttp.open(GET, QUEST_GLOBAL_SURVEY_START_URL, true); // true for asynchronous 

	xmlHttp.send();
}

function extractGlobalWord(responseText) {

	var jsonObj = JSON.parse(responseText);

	if(responseText == null || jsonObj == null || jsonObj.word == undefined) {
		
		document.getElementById("survey_input_container").style.visibility = "hidden"
		document.getElementById("no_survey_img").style.visibility = "visible"
		document.getElementById("word").innerHTML = '';
		document.getElementById("question").innerHTML = 'Looks like there\'s no info coming from the server right now';
	} else {
	
		document.getElementById("word").innerHTML = jsonObj.word.capitalizeFirstLetter();
		enableView();
	}
}

function putGlobalWord() {

	var radioYes = document.getElementById("yes");
	var radioNo = document.getElementById("no");

	if(!radioYes.checked && !radioNo.checked) {

		alert("Opps! Looks like you forgot to check a box");
		return;
	}

	var word = document.getElementById("word").innerHTML;

	var URL = makeGlobalURL(word, radioYes.checked);

	var xmlHttp = new XMLHttpRequest();

	xmlHttp.open(GET, URL, true); // true for asynchronous 

	xmlHttp.send();

	// finish();

	loadView();

	getGlobalWord();
}

function loadView() {

	document.getElementById("yes").disabled = true;
	document.getElementById("no").disabled = true;
	
	var submitButton = document.getElementById("submitButton");
	submitButton.className = submitButton.className + " disabled";
	submitButton.disabled = true;

	document.getElementById("word").innerHTML = "..."
}

function enableView() {

	document.getElementById("yes").disabled = false;
	document.getElementById("no").disabled = false;
	
	var submitButton = document.getElementById("submitButton");
	submitButton.className = submitButton.className.replace(/(?:^|\s)disabled(?!\S)/g, " enabled");
	submitButton.disabled = false;
}

function makeGlobalURL(word, isHard) {

	var isHardParam = " ";

	if(isHard == true) {
		isHardParam = isHard;
	}
	
	var url = QUEST_GLOBAL_SURVEY_CONTINUE_URL + word + QUEST_GLOBAL_SURVEY_CONTINUE_URL_SECOND_PARAM + isHardParam;

	return url;
}

function finish() {

	document.getElementById("survey_input_container").style.visibility = "hidden"
	document.getElementById("word").innerHTML = '';
	document.getElementById("question").innerHTML = 'Thanks for your input!!';
}

String.prototype.capitalizeFirstLetter = function() {
	return this.charAt(0).toUpperCase() + this.slice(1);
}

function addCloseEvent() {

	window.addEventListener("beforeunload", function (e) {


		// var confirmationMessage = "\o/";

		// (e || window.event).returnValue = confirmationMessage; //Gecko + IE
		// // alert(e.returnValue);                       //Webkit, Safari, Chrome
	});
}

addCloseEvent();
getGlobalWord();