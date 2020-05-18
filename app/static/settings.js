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
	Object.keys(data).map( key => {
		console.log('checking for', key)
		if (document.getElementById(key) != null) {
			console.log('setting',key,data[key])
			document.getElementById(key).value = data[key]
		}
	})
}
