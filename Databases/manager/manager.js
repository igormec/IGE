var currentNode = null;
var columns = 0;
var tableHeight = 0;
var selected = []

function updateJSON(){

	var arr = selected;
	var newjson = "";

	arr.forEach(function(e){
		newjson += e;
		var index = arr.indexOf(e);
		index+1 == arr.length ? newjson += " <br>" : newjson += ", <br>";
	});

	
	$("#jsonList").html(newjson);
	//var newjson = oldjson.length == 0 ? "<br>" + txt : oldjson + ",<br>" + txt;

	//$("#jsonList").html(newjson);
}

function selectProfile(prof){

	var txt = $(prof).parent('.mainListItem').find('p.profhandle').text();

	if(selected.includes(txt)){
		selected.splice(selected.indexOf(txt), 1);
		updateJSON();
		enableHover(prof);
		$(prof).parent('.mainListItem').animate({"backgroundColor":"#444444"}, 100);
	}else{
		selected.push(txt);
		updateJSON();
		$(prof).parent('.mainListItem').unbind('mouseenter mouseleave');
		$(prof).parent('.mainListItem').animate({"backgroundColor":"#417f50"}, 100);
	
	}

	// console.log(selected.length);

	// updateJSON();
	// $(prof).parent('.mainListItem').unbind('mouseenter mouseleave');
	// $(prof).parent('.mainListItem').animate({"backgroundColor":"#417f50"}, 100);

}


function enableHover(prof){

	$(prof).parent('.mainListItem').bind({
		mouseenter: function() {
		$(this).animate({"backgroundColor":"#252525"}, 100);
		//alert("IN");
		},
		mouseleave: function() {
		$(this).animate({"backgroundColor":"#494949"}, 100);
		//alert("OUT");
		}
	});
}

function addEvents(){


	$(".mainListItem").hover(
		function() {
			$(this).animate({"backgroundColor":"#252525"}, 100);
			//alert("IN");
		},
		function() {
			$(this).animate({"backgroundColor":"#494949"}, 100);
			//alert("OUT");
		}
	);

	// $(".mainListItem").click(
	// 	function() {
	// 		window.open('https://instagram.com/igor.mec', '_blank'); 		
	// 	}
	// );

	$(".profimg").click(
		function() {
			selectProfile(this);			
		}
	);
}


document.addEventListener('DOMContentLoaded', function () {
  	addEvents();	
});





















// function makeTable(nodeList) {

// 	var $table = $("#bmTable");
// 	$table.remove();
// 	$("#bm-list").append($("<table>", {"id":"bmTable"}))
// 	$table = $("#bmTable");
// 	$tbody = $("<tbody>");
// 	$table.append($tbody);
// 	//nuclear option
// 	//$table.html("");
// 	console.log(nodeList.length);

// 	//Go through all the nodes at the current BookmarkNode
// 	for(var i = 0;i < (nodeList.length);i++){
// 		var node = nodeList[i];
// 		//Add a new row every 5 nodes, makes 5 columns.
// 		if(i % 5 == 0){
// 			var $row = $("<tr>");
// 			$tbody.append($row);
// 		}
// 		//Make a td element
// 		//make the mainListItem div inside td
// 		var $td = $("<td>");

// 		if (node.url){
// 			$td.append(makeLinkDiv(node));
// 		}else{
// 			$td.append(makeGroupDiv(node));
// 		}
// 		//After adding 5 nodes to row, append row to table
// 		$row.append($td);
// 	}
// 	//Refresh all the divs functionalities
// 	addEvents();
// }


// function makeLinkDiv(node){
// 	var $itemDiv = $("<div>", {"class":"mainListItem", "id":node.id});
// 	var $span = $("<p>", {"class":"listItemLink"}).append(node.title ? node.title : node.url);
// 	$itemDiv.append($span);
// 	return $itemDiv;
// }

// function makeGroupDiv(node){
// 	var $itemDiv = $("<div>", {"class":"mainListItem", "id":node.id});
// 	var $span = $("<p>", {"class":"listItemLink"}).append(node.title ? node.title : "Group");
// 	$itemDiv.append($span);
// 	return $itemDiv;
// }

// function makeInfoBar(node){
// 	var $itemDiv = $("<div>", {"class":"mainListItem", "id":node.id});
// 	var $span = $("<p>", {"class":"listItemLink"}).append(node.title ? node.title : node.url);
// 	$itemDiv.append($span);
// 	return $itemDiv;
// }

// function setSizes(){
// 	console.log("Changing size");
// 	var width = window.innerWidth;
// 	var height = window.innerHeight;
// 	oldCols = columns;
// 	oldTblHeight = tableHeight;
// 	columns = Math.ceil(width*0.7)/240;
// 	tableHeight = Math.ceil(height*0.7);

// 	//Change the table and row values and reload doc
// 	//only if at least one of them has changed
// 	if(!(columns == oldCols && tableHeight == oldTblHeight)){
// 		console.log("Changing size for real");
// 		var node = chrome.bookmarks.getSubTree(currentNode.id,
// 			function(node){
// 				node = node[0];
// 				makeTable(node.children);
// 			}
// 		);
// 	}	
// }



// function makeInforBar(node){
// 	$("#infoPanTitle").html(node.title ? node.title : "NO TITLE");
// 	$("#infoPanURL").html(node.url ? node.url : node.children.length + " children");

// 	if(node.url){
// 		$("#infoPanIcon").css("backgroundColor","#FFFFFF");	
	
// 	}else{
// 		$("#infoPanIcon").css("backgroundColor","#3585D9");
// 	}
	
	
// 	if (node.dateAdded){
// 		var date = new Date(node.dateAdded);
// 		date = (getMonthString(date.getMonth()) + ' ' + getDateEnd(date.getDate()) +' '+  date.getFullYear());
// 		$("#infoPanAddDate").html(node.url ? "Added on: " + date : "Created on: "+ date);
	
// 	}else{
// 		$("#infoPanAddDate").html(node.url ? "Added on: NO DATE" : "Created on: NO DATE");
// 	}

// }



//window.addEventListener("resize", setSizes);












/*

//UNUSED

//Goes through the list returned by chrome.bookmarks.getTree()
function parseNodes(nodeList){
	var $table = $("#bmTable");

	for(var i = 0;i < Math.ceil(nodeList.length/4);i++){

		var $row = $("<tr>");
		for(var j = 0; j < 4;j++){
			$row.append(showNode(nodeList[i]));
		}
	}
	return list;
}

//Extracts the data from each individual bookmarkNode
function showNode(node){
	if(node.title){
		/*var anc = $("<a>");
		anc.attr("href", node.url
		anc.text(node.title);
		var span = $("<span>");
		span.append(anc).append(" - " +new Date(node.dateAdded));/////*

		var $listDiv = $("<div>", {"class":"mainListItem"});
		$listDiv.append(node.title);
		var $td = $("<td>");
		$td.append($listDiv);

	}
	//var li = $(node.title ? "<li>" : "<div>").append(span);
	
	//For folders, recurse into parseNodes to read the childrenNodeTree
	if (node.children && node.children.length > 0){
		li.append(parseNodes(node.children));
	}
	return li;
}









/*function getMainSubTree() {
	var tree = chrome.bookmarks.getTree(
		function(tree){
			tree = tree.getChildren();
		});

	return tree;
}*/

//Shows all bookmarks as a list of links
/*function showAll(){
	var allNodes = chrome.bookmarks.getTree(function(allNodes){
		$("#bm-list").append(parseNodes(allNodes));
	});
}*/