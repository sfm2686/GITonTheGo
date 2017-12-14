$.getJSON("http://127.0.0.1:5000/api/v1/git/stats",
	function(data) {

		// Getting the body of the response
		data = data["data"];

		// Populating table 0 (user percentage)
		var currentTable = data["table0"];
		var keys = Object.keys(currentTable);
		popTable("stat0Table", currentTable, keys);

		// Populating table 1 (day percentage)
		currentTable = data["table1"];
		keys = Object.keys(currentTable);
		popTable("stat1Table", currentTable, keys);
		
		// Populating table 2 (day percentage)
		currentTable = data["table2"];
		keys = Object.keys(currentTable);
		popTable("stat2Table", currentTable, keys);

		// Populating table 3 (common commit word)
		currentTable = data["table3"];
		keys = Object.keys(currentTable);
		popTable("stat3Table", currentTable, keys);
	});

function popTable(tableID, data, keys) {

	// Making empty arrays for both values and keys
	keysAr = [];
	values = [];

	// Pushing both values and keys of the data to the newly made arrays
	for (var i = 0; i < keys.length; i ++) {
		keysAr.push(keys[i]);
		values.push(data[keys[i]]);
	}

	var max = 0;
	var index = 0;
	for (var i = 0; i < keys.length; i ++) {

		// Finding the max value and its index to append to the html, so the tables are sorted
		max = Math.max.apply(Math, values);
		index = values.indexOf(max);

		// Checking to see if the '%' should be part of the append
		if (tableID == "stat3Table") {
			$("#" + tableID).append("<tr><td>" + keysAr[index] + "</td><td>" + max + "</td></tr>");
		} else {
			$("#" + tableID).append("<tr><td>" + keysAr[index] + "</td><td>" + max + "%</td></tr>");
		}
		// Deleted values already appended
		values.splice(index, 1);
		keysAr.splice(index, 1);
	}
}

function goToShell() {
  // flask api calls happen here
}