$.getJSON("http://127.0.0.1:5000/api/v1/git/stats",
	function(data) {

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
	for (var i = keys.length - 1; i >= 0; i --) {
		$("#" + tableID).append("<tr><td>" + keys[i] + "</td><td>" + data[keys[i]] + "%</td></tr>");
	}
}

function goToShell() {
  // flask api calls happen here
}