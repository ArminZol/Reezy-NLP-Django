function getUserWord() {
	var xmlHttp = new XMLHttpRequest();

	xmlHttp.onreadystatechange = function() {

		if (xmlHttp.readyState == 4) {

			if(xmlHttp.status == 200) {
			
				extractUserWord(xmlHttp.responseText, false);
			} else {

				extractUserWord(null, false);
			}
		}
	}

	xmlHttp.open(GET, QUEST_USER_SURVEY_START_URL, true); // true for asynchronous 

	xmlHttp.send();
}

function extractUserWord(responseText, showContext) {

	var jsonObj = JSON.parse(responseText);

	if(responseText == null || jsonObj == null || jsonObj.word == undefined) {
		
		document.getElementById("user_survey_input_container").style.visibility = "hidden"
		document.getElementById("user_word").innerHTML = '';
		document.getElementById("user_question").innerHTML = 'Looks like there\'s no info coming from the server right now';
	} else {
		
		if(showContext) {

			document.getElementById("user_survey_input_container").style.visibility = "visible";
			document.getElementById("user_question").style.visibility = "visible";	
		}
		
		document.getElementById("user_word").innerHTML = jsonObj.word.capitalizeFirstLetter();
	}
}

function putUserWord() {
	var radioYes = document.getElementById("user_yes");
	var radioNo = document.getElementById("user_no");

	if(!radioYes.checked && !radioNo.checked) {

		alert("Oops! Looks like you forgot to check a box");
		return;
	}

	var word = document.getElementById("user_word").innerHTML;

	var URL = makeUserURL(word, radioYes.checked);

	var xmlHttp = new XMLHttpRequest();

	xmlHttp.onreadystatechange = function() {

		if (xmlHttp.readyState == 4) {

			if(xmlHttp.status == 200) {
			
				extractUserWord(xmlHttp.responseText, true);
			} else {

				extractUserWord(null, false);
			}
		}
	}

	xmlHttp.open(GET, URL, true); // true for asynchronous 

	xmlHttp.send();

	setInBetweenText();
}

function makeUserURL(word, isHard) {

	var isHardParam = " ";

	if(isHard == true) {
		isHardParam = isHard;
	}

	var url = QUEST_USER_SURVEY_CONTINUE_URL + word + QUEST_USER_SURVEY_CONTINUE_URL_SECOND_PARAM + isHardParam;

	return url;
}

String.prototype.capitalizeFirstLetter = function() {
	return this.charAt(0).toUpperCase() + this.slice(1);
}

function setInBetweenText() {

	document.getElementById("user_survey_input_container").style.visibility = "hidden"
	document.getElementById("user_word").innerHTML = 'Loading Next Word...';
	document.getElementById("user_question").innerHTML = 'What About This One?';
	document.getElementById("user_question").style.visibility = "hidden";
}

// getUserWord();