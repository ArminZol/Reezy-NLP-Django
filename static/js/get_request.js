last_text = "";

function beginSimplification() {
	document.getElementById("statistics").innerHTML = null;
	document.getElementById("definition").innerHTML = null;
	load(false);

	httpGetAsync(true, 'text');
}

 function findDefinition(value) {
 	createLoader()
	httpGetAsync(false, value);
 }

function httpGetAsync(isSimplification, value) {
	var text = value;
	if (isSimplification) { 
		text = document.getElementById(value).value;
	}

	if(text === null || text == "") {

		load(true);

		return;
	}

	// showQuestion();

	var xmlHttp = new XMLHttpRequest();

	xmlHttp.onreadystatechange = function() {

		if (xmlHttp.readyState == 4) {

			if(xmlHttp.status == 200) {

				if (isSimplification) { sortResponse(xmlHttp.responseText); }
				else { sortDefinitionResponse(xmlHttp.responseText); }
			} else {

				sortResponse(null);
			}

			load(true);
		}
	}

	var url = QUEST_DICT_URL + text;
	if (isSimplification) { url = makeURL(text); }

	xmlHttp.open(GET, url, true); // true for asynchronous 

	xmlHttp.send();
}

function makeURL(text) {

	var local_quest_simp_url = QUEST_SIMP_URL;

	var split = text.split(" ");

	var i;

	for (i = 0; i < split.length; i++)
		local_quest_simp_url += split[i] + "+";

	return local_quest_simp_url;
}

function makeSentence(text) {
	document.getElementById("simplification_result").innerHTML = '';

	var split = text.split(" ");
	for (var i = 0; i < split.length; i++)
	{
		if (split[i] != null)
		{
			const word = split[i].replace(/\.$/, "");
			var element = document.createElement("span");
			element.innerHTML = split[i];
			element.onclick = function(){
				findDefinition(word);
			};
			element.className = "word-container left-right";
			document.getElementById("simplification_result").appendChild(element);

			element = document.createElement("span");
			element.innerHTML = " ";
			document.getElementById("simplification_result").appendChild(element);
		}
	}
}

function sortResponse(response) {
	
	if (response == null || JSON.parse(response).html == "True") {

		var ERR = "An error occured while simplifying your sentence";

		document.getElementById("simplification_result").innerHTML = ERR;
	} else {

		var jsonObj = JSON.parse(response);

		makeSentence(jsonObj.simplification_result);

		var time = new String("Total Time: ").bold();

		document.getElementById("statistics").innerHTML = jsonObj.statistics;

		document.getElementById("time").innerHTML = time + jsonObj.time;

		last_text = jsonObj.simplification_result;
	}
}

function sortDefinitionResponse(response) {
	if (response != null) {
		var jsonObj = JSON.parse(response);

		var string = "" ;

		for (var value in jsonObj)
		{
			if (jsonObj[value].trim() != "")
			{
				string += value.bold() + jsonObj[value] + "\n";
			}
		}

		var htmlString = string.replace(/(\n)/gm, "<br>")

		document.getElementById("definition").innerHTML = htmlString;
	}
}

function createLoader() {
	document.getElementById("definition").innerHTML = 
	'<center> \
		<div class="row"></div> \
		<div id="loading" class="preloader-wrapper big active"> \
			<div class="spinner-layer"> \
				<div class="circle-clipper left"> \
					<div class="circle"></div> \
				</div> \
				<div class="gap-patch"> \
					<div class="circle"></div> \
				</div> \
				<div class="circle-clipper right"> \
					<div class="circle"></div> \
				</div> \
			</div> \
		</div> \
	</center>';
}

function load(stop) {

	var loader = document.getElementById("loading");

	if(stop == true) {

		loader.className = loader.className.replace(/(?:^|\s)active(?!\S)/g, " inactive");
	} else {

		loader.className = loader.className.replace(/(?:^|\s)inactive(?!\S)/g, " active");
	}
}

function showQuestion() {

	if(document.getElementById("user_word").innerHTML != '' && document.getElementById("user_word").innerHTML != DEAFULT_WORD_FOR_SURVEY) {

		document.getElementById("user_survey").style.visibility = "visible"
	}
}