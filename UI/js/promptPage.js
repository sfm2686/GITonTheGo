// Lang versions //

// Java versions
var javaVersions = ["Java 8", "Java 7"];

// Python versions
var pythonVersions = ["Python 3", "Python 2"];

// Ruby versions
var rubyVersions = ["Ruby 2", "Ruby 1"];


// Lang frameworks //

// Java frameworks
var javaFrameworks = ["Spark", "Vaadin"]

// Python frameworks
var pythonFrameworks = ["Flask", "Djnago"]

// Ruby frameworks
var rubyFrameworks = ["Sinatra", "CakePHP"]


// Making maps for lang versions and frameworks
var versionMap = new Object();
var frameworkMap = new Object();

// populating version and framework maps
versionMap["N/A"] = [];
versionMap["Java"] = javaVersions;
versionMap["Python"] = pythonVersions;
versionMap["Ruby"] = rubyVersions;

frameworkMap["N/A"] = [];
frameworkMap["Java"] = javaFrameworks;
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

	var newOption = document.createElement("option");
	newOption.textContent = "N/A";
	newOption.value = "N/A";
	frSelect.appendChild(newOption);

	for (var i = 0; i < frArray.length; i ++) {
		var optionText = frArray[i];
		var newOption = document.createElement("option");
		newOption.textContent = optionText;
		newOption.value = optionText;
		frSelect.appendChild(newOption);
	}
}

function submitted() {
	// flask api calls happen here
	window.location.href = "/shellPage.html";
	window.alert("redirected")
}