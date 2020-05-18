#'/get_json_settings'

getsettings()

function getsettings() {
	$.ajax({
  		dataType: "json",
  		url: "/get_json_settings",
  		success: function( data ) {updatestatus( data );},
		failure: function(errMsg) {console.log('failed');}
	});
}

function updatestatus( data ) {
	data.keys().map( key => {
		document.getElementById(key).value = data[key]
	})
}
