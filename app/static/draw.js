
//var canv = document.createElement('canvas');
//canv.id = 'someId';
//document.body.appendChild(canv);

getupdate()

function getupdate() {
	$.ajax({
  		dataType: "json",
  		url: "/svgfiles",
  		success: function( data ) { updatestatus( data ) }
	});
}

function updatestatus( data ) {
	console.log( data )
	var opt = document.createElement('option')
	opt.appendChild( document.createTextNode('New Option Text') );
	opt.value = 'option value';
	document.getElementById("svg_list").appendChild( opt )
}

