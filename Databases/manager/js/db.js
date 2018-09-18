var dbFileElm = document.getElementById('dbfile');
var outputElm = document.getElementById('output');
var errorElm = document.getElementById('error');
var savedbElm = document.getElementById('savedb');



// Start the worker in which sql.js will run
var worker = new Worker("./js/lib/worker.sql.js");
worker.onerror = error;


// Open a database
worker.postMessage({ action: 'open' });

// Connect to the HTML element we 'print' to
function print(text) {
	outputElm.innerHTML = text.replace(/\n/g, '<br>');
}

function error(e) {
	console.log(e);
	errorElm.style.height = '2em';
	errorElm.textContent = e.message;
}

function noerror() {
	errorElm.style.height = '0';
}


function execute(commands) {
	worker.onmessage = function (event) {
		var results = event.data.results;
		console.log("Executing SQL");

		outputElm.innerHTML = "";
		var text = $("#outputElm").html();
		var lis = []
		console.log(results);
		for (var i = 0; i < results.length; i++) {

			outputElm.appendChild(tableCreate(results[i].columns, results[i].values));
			makeTable(results[i].values)

			console.log("Displaying results");
		}

		var c = "SELECT * FROM following;"
		worker.postMessage({ action: 'exec', sql: c });
		outputElm.textContent = "Fetching results...";
	}












	function makeTable(dataArr) {

		var $table = $("#profTable");
		$table.remove();
		$("#main-grid").append($("<table>", { "id": "profTable" }))
		$table = $("#profTable");
		$tbody = $("<tbody>");
		$table.append($tbody);
		//nuclear option
		//$table.html("");
		console.log(dataArr.length);

		//Go through all the nodes at the current BookmarkNode
		for (var i = 0; i < (dataArr.length); i++) {
			//Add a new row every 5 nodes, makes 5 columns.
			if (i % 5 == 0) {
				var $row = $("<tr>");
				$tbody.append($row);
			}
			//Make a td element
			//make the mainListItem div inside td
			var $td = makeProfileDiv(dataArr[i]);
			//$td.append();


			//After adding 5 nodes to row, append row to table
			$row.append($td);
		}
		//Refresh all the divs functionalities
		addEvents();
	}







	function makeProfileDiv(prof) {
		var $itemDiv = $("<td>", { "class": "mainListItem", "id": prof[0] });
		var $pic = $("<img>", { "src": prof[3], "class": "profimg", "width": "85", "height": "85" });
		var $handle = $("<p>", { "class": "profhandle" }).append(prof[1]);
		var $name = $("<p>", { "class": "profname" }).append(prof[2]);

		$itemDiv.append($pic);
		$itemDiv.append($handle);
		$itemDiv.append($name);

		return $itemDiv;
	}

	function execSQL() {
		noerror()
		var command = "SELECT `name`, `sql`\n  FROM `sqlite_master`\n  WHERE type='table';";
		execute(command);
	}



	// Load a db from a file
	dbFileElm.onchange = function () {
		console.log("Loading new DB: " + dbFileElm.files[0]);
		var f = dbFileElm.files[0];
		var r = new FileReader();
		r.onload = function () {
			worker.onmessage = function () {
				// Show the schema of the loaded database
				console.log("in OnMessage");
				execSQL();
			};
			//worker.onmessage = function () {};
			try {
				console.log(r.result);
				worker.postMessage({ action: 'open', buffer: r.result }, [r.result]);
				console.log(r.result);
			}
			catch (exception) {
				console.log("catch");
				worker.postMessage({ action: 'open', buffer: r.result });
			}
		}
		r.readAsArrayBuffer(f);
	}

	// Save the db to a file
	function savedb() {
		worker.onmessage = function (event) {
			var arraybuff = event.data.buffer;
			var blob = new Blob([arraybuff]);
			var a = document.createElement("a");
			a.href = window.URL.createObjectURL(blob);
			a.download = "sql.db";
			a.onclick = function () {
				setTimeout(function () {
					window.URL.revokeObjectURL(a.href);
				}, 1500);
			};
			a.click();
		};
		worker.postMessage({ action: 'export' });
	}
	savedbElm.addEventListener("click", savedb, true);