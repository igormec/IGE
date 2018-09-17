var dbFileElm = document.getElementById('dbfile');
var outputElm = document.getElementById('output');
var errorElm = document.getElementById('error');
var savedbElm = document.getElementById('savedb');



// Start the worker in which sql.js will run
var worker = new Worker("./js/lib/worker.sql.js");
worker.onerror = error;


// Open a database
worker.postMessage({action:'open'});

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
	worker.onmessage = function(event) {
		var results = event.data.results;
        console.log("Executing SQL");

		outputElm.innerHTML = "";
		for (var i=0; i<results.length; i++) {
			outputElm.appendChild(tableCreate(results[i].columns, results[i].values));
		}
		console.log("Displaying results");
	}

	var c = "SELECT username FROM audi;"
	worker.postMessage({action:'exec', sql:commands});
	outputElm.textContent = "Fetching results...";
}


// Create an HTML table
var tableCreate = function () {
    function valconcat(vals, tagName) {
      if (vals.length === 0) return '';
      var open = '<'+tagName+'>', close='</'+tagName+'>';
      return open + vals.join(close + open) + close;
    }
    return function (columns, values){
      var tbl  = document.createElement('table');
      var html = '<thead>' + valconcat(columns, 'th') + '</thead>';
      var rows = values.map(function(v){ return valconcat(v, 'td'); });
      html += '<tbody>' + valconcat(rows, 'tr') + '</tbody>';
        tbl.innerHTML = html;
      return tbl;
    }
  }();

function execEditorContents () {
    noerror()
    var command = "SELECT `name`, `sql`\n  FROM `sqlite_master`\n  WHERE type='table';";
	execute (command);
}



// Load a db from a file
dbFileElm.onchange = function() {
    console.log("new DB detected");
	var f = dbFileElm.files[0];
	var r = new FileReader();
		r.onload = function(){
		worker.onmessage = function () {
			// Show the schema of the loaded database
			console.log("in OnMessage")			;
//			execEditorContents();
		};
		//worker.onmessage = function () {};
		try {
			console.log("try");
			worker.postMessage({action:'open',buffer:r.result}, [r.result]);
		}
		catch(exception) {
			console.log("catch");
			worker.postMessage({action:'open',buffer:r.result});
		}
	}
	console.log("end");
	r.readAsArrayBuffer(f);
}

// Save the db to a file
function savedb () {
	worker.onmessage = function(event) {
		var arraybuff = event.data.buffer;
		var blob = new Blob([arraybuff]);
		var a = document.createElement("a");
		a.href = window.URL.createObjectURL(blob);
		a.download = "sql.db";
		a.onclick = function() {
			setTimeout(function() {
				window.URL.revokeObjectURL(a.href);
			}, 1500);
		};
		a.click();
	};
	worker.postMessage({action:'export'});
}
savedbElm.addEventListener("click", savedb, true);