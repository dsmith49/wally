
//var canv = document.createElement('canvas');
//canv.id = 'someId';
//document.body.appendChild(canv);

getupdate()
document.getElementById("svg_list").onchange = function(){loadsvg()}

function loadsvg() {
	//var img = document.createElement('IMG')
	console.log(document.getElementById("svg_image"))
	var select = document.getElementById("svg_list")
	console.log(select)
	var filename = select.options[select.selectedIndex].value
	var astring = "{{url_for('static', filename='images/" + filename + "')}}"
	var bstring = 'static/images/' + filename
	//img.src = '"' + astring + '"'
	console.log( document.getElementById("svg_image") )
	document.getElementById("svg_image").src = bstring























	//document.getElementById("svg_container").removeChild( document.getElementById("svg_container").childNodes[0] )
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

