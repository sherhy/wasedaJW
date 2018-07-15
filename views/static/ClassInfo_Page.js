function add() {
	document.getElementById("flashMessage").innerHTML ="<div class='alert alert-success alert-dismissible'> <strong>Success!</strong> You have added this course to your timetable</div>";

}
var addButton = document.getElementById("addButton");
addButton.addEventListener("click",	add);