// Lang versions //

// Python versions
var pythonVersions = ["Python 3", "Python 2"];

// Ruby versions
var rubyVersions = ["Ruby 2", "Ruby 1"];


// Lang frameworks //

// Python frameworks
var pythonFrameworks = ["N/A", "Flask", "Djnago"]

// Ruby frameworks
var rubyFrameworks = ["N/A", "Sinatra", "CakePHP"]


// Making maps for lang versions and frameworks
var versionMap = new Object();
var frameworkMap = new Object();

// populating version and framework maps
versionMap["N/A"] = ["-"];
versionMap["Python"] = pythonVersions;
versionMap["Ruby"] = rubyVersions;

frameworkMap["N/A"] = ["-"];
frameworkMap["Python"] = pythonFrameworks;
frameworkMap["Ruby"] = rubyFrameworks;

function versionPop() {
	// Select element
	var langSelect = document.getElementById("lang");

	// version select element
	var versionSelect = document.getElementById("version")

	// getting the right version array
	var versionArray = versionMap[langSelect.options[langSelect.selectedIndex].value];

	versionSelect.options.length = 0;

	for (var i = 0; i < versionArray.length; i ++) {
		var optionText = versionArray[i];
		var newOption = document.createElement("option");
		newOption.textContent = optionText;
		newOption.value = optionText;
		versionSelect.appendChild(newOption);
	}
}

function frameworkPop() {
	// Select element
	var langSelect = document.getElementById("lang");

	// framework select element
	var frSelect = document.getElementById("framework")

	// getting the right framework array
	var frArray = frameworkMap[langSelect.options[langSelect.selectedIndex].value];

	frSelect.options.length = 0;


	for (var i = 0; i < frArray.length; i ++) {
		var optionText = frArray[i];
		var newOption = document.createElement("option");
		newOption.textContent = optionText;
		newOption.value = optionText;
		frSelect.appendChild(newOption);
	}
}

function submitted() {
	if (document.getElementById("repoLink").value != '') {
		$("#submitButton").attr("href", "shellPage.html");
	} else {
		alert("Where are you going? You did not give us a repository yet!");
	}
	// TODO - add code for failure
	var data = {};
	data["language"] = document.getElementById("lang").options[document.getElementById("lang").selectedIndex].value;
	data["version"] = document.getElementById("version").options[document.getElementById("version").selectedIndex].value;
	data["framework"] = document.getElementById("framework").options[document.getElementById("framework").selectedIndex].value;
	data["libraries"] = document.getElementById("libraries").value.split(',');
	data["repoLink"] = document.getElementById("repoLink").value;

	$.ajax({
		url: "http://127.0.0.1:5000/api/v1/init",
		data: JSON.stringify(data),
		contentType: 'application/json',
		type: 'POST',
		success: function() {
			console.log("success");
		},
		error: function() {
			console.log("error");
		}
	});
}

function tryit() {
	// flask api calls for 'try it', pre-built project here
}