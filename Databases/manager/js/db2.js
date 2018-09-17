var dbFileElm = document.getElementById('dbfile');

var sql = $.getScript("sql.js");
var db = new sql.Database();


dbFileElm.onchange = () => {
    var f = dbFileElm.files[0];
    var r = new FileReader();
    r.onload = function() {
      var Uints = new Uint8Array(r.result);
      db = new SQL.Database(Uints);
    }
    r.readAsArrayBuffer(f);
  }