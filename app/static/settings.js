getsettings()

function getsettings() {
	console.log('getting seetings')
	$.ajax({
  		dataType: "json",
  		url: "/get_json_settings",
  		success: function( data ) {updatestatus( data );},
		failure: function(errMsg) {console.log('failed');}
	});
}

function updatestatus( data ) {
	console.log('updating seetings')
	Object.keys(data).map( key => {
		document.getElementById(key).value = data[key]
	})
}
