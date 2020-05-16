
//var canv = document.createElement('canvas');
//canv.id = 'someId';
//document.body.appendChild(canv);

getupdate()
document.getElementById("svg_list").onchange = function(){loadsvg()}

function loadsvg() {
	var img = createElement('IMG')
	var filename = document.getElementById("svg_list").options[e.selectedIndex].value
	img.src = "{{url_for('static', filename='" + filename + "')}}"
	document.getElementById("svg_container").remove(0)
	document.getElementById("svg_container").appendChild( img )
}
function getupdate() {
	$.ajax({
  		dataType: "json",
  		url: "/svgfiles",
  		success: function( data ) { updatestatus( data ) }
	});
}

function updatestatus( data ) {
	console.log( data )
	var sel = document.getElementById('svg_list');
	for (i = sel.length - 1; i >= 0; i--) {
		sel.remove(i);
	}
	data.map( filename => {
		var opt = document.createElement('option')
		opt.appendChild( document.createTextNode(filename) );
		opt.value = filename;
		document.getElementById("svg_list").appendChild( opt )
	})
}

