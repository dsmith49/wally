document.getElementById("save_button").onclick = function(){sendsettings()}

var datakeys = null
getsettings()

function getsettings() {
	$.ajax({
  		dataType: "json",
  		url: "/get_json_settings",
  		success: function( data ) {updatestatus( data );},
		failure: function(errMsg) {console.log('failed');}
	});
}

function sendsettings() {
	var dict = {}
	datakeys.map( key => {
		if (document.getElementById(key) != null) {
			dict[key] = document.getElementById(key).value
		}
	})
	console.log('in send settings', dict)
	$.ajax({
    	type: "POST",
  		url: "/get_json_settings",
		data : JSON.stringify( dict ),
    	contentType: "application/json; charset=utf-8",
    	dataType: "json",
  		success: function( data ) {console.log('success')},
		failure: function(errMsg) {console.log('failed');}
	});
}

function updatestatus( data ) {
	if (datakeys == null) {datakeys = Object.keys(data)}
	Object.keys(data).map( key => {
		if (document.getElementById(key) != null) {
			document.getElementById(key).value = data[key]
		}
	})
}
