function edit() {
	
	if(document.getElementById("edit_fab").innerHTML == "mode_edit" || document.getElementById("edit_fab_mobile").innerHTML == "mode_edit") {
		
		document.getElementById("first_name").disabled = false;
		document.getElementById("last_name").disabled = false;
		document.getElementById("username").disabled = false;
		document.getElementById("email").disabled = false;

		document.getElementById("edit_fab").innerHTML = 'done';
		document.getElementById("edit_fab_mobile").innerHTML = 'done';
	} else {

		document.getElementById("edit_form").submit();
	}
}