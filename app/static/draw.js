var interval = null

getupdate(false)
document.getElementById("svg_list").onchange = function(){loadsvg()}
document.getElementById("draw_button").onclick = function(){call_draw()}
document.getElementById("stop_button").onclick = function(){call_stop()}

function call_draw() {
	var svglist = document.getElementById("svg_list")
	var filename = svglist.options[ svglist.selectedIndex ].value
	$.ajax({
		type: "POST",
		url: "/draw_svg",
		data: JSON.stringify( filename ),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function(data){
			interval = setInterval(function() {getupdate(true)}, 5000);
		},
		failure: function(errMsg) {console.log('failed');}
	});
}

function call_stop() {
	$.ajax({
		type: "POST",
		url: "/stop_draw_svg",
		contentType: "application/json; charset=utf-8",
		success: function(data){ console.log('success'); clearInterval(interval)},
		failure: function(errMsg) {console.log('failed');}
	});	
}

function loadsvg() {
	var select = document.getElementById("svg_list")
	var filename = select.options[select.selectedIndex].value
	var bstring = 'static/images/' + filename
	document.getElementById("svg_image").src = bstring
}

function getupdate( bar ) {
	console.log('getting update',bar)
	$.ajax({
  		dataType: "json",
  		url: "/svgfiles",
  		success: function( data ) {
			if (!bar) {updatestatus( data );};
			if (bar) {updateprogress( data );};
		},
		failure: function(errMsg) {console.log('failed');}
	});
}

function updatestatus( data ) {
	var sel = document.getElementById('svg_list');
	for (i = sel.length - 1; i >= 0; i--) {
		sel.remove(i);
	}
	data['filenames'].map( filename => {
		var opt = document.createElement('option')
		opt.appendChild( document.createTextNode(filename) );
		opt.value = filename;
		document.getElementById("svg_list").appendChild( opt )
	})
	document.getElementById("svg_list").selectedIndex = 0
	loadsvg()
}

function updateprogress( data ) {
	console.log( 'update progress', data['progress'] )
	var sel = document.getElementById('progress_bar');
	sel.innerHTML = data['progress'][0].toString() + ' of ' + data['progress'][1].toString()
}

