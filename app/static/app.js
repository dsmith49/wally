
//var canv = document.createElement('canvas');
//canv.id = 'someId';
//document.body.appendChild(canv);

function getupdate() {
	$.ajax({
  		dataType: "json",
  		url: "/status",
  		success: function( data ) { updatestatus( data ) }
	});
}

function updatestatus( data ) {
	document.getElementById("power_val").innerHTML = data['power']
	document.getElementById("pen_val").innerHTML = data['pendown']
	document.getElementById("velocity_0").innerHTML = data['velocity'][0]
	document.getElementById("velocity_1").innerHTML = data['velocity'][1]
}

document.addEventListener('keydown', function(e) {
	if (document.activeElement === document.body ) {	
		var code = e.which || e.keyCode;
		var command = null
		if (([38,87]).includes(code)) { command = 'UP' }
		if (([88,40]).includes(code)) { command = 'DOWN' }
		if (([65,37]).includes(code)) { command = 'LEFT' }
		if (([39,68]).includes(code)) { command = 'RIGHT' }
		if (([81]).includes(code)) { command = 'UPLEFT' }
		if (([69]).includes(code)) { command = 'UPRIGHT' }
		if (([90]).includes(code)) { command = 'DOWNLEFT' }
		if (([67]).includes(code)) { command = 'DOWNRIGHT' }
		if (([83,32]).includes(code)) { command = 'STOP' }
		if (([221]).includes(code)) { command = 'PENUP' }
		if (([219]).includes(code)) { command = 'PENDOWN' }
		if (([49]).includes(code)) { command = 'PEN1' }
		if (([50]).includes(code)) { command = 'PEN2' }
		if (([51]).includes(code)) { command = 'PEN3' }
		if (([192]).includes(code)) { command = 'POWER' }
		if (([80]).includes(code)) { command = 'CALIBRATE' }
		if (([27]).includes(code)) { command = 'END' }
		console.log(command)
		if (command != null) {
			command_dict = new Object();
			command_dict['command'] = command
			$.ajax({
    			type: "POST",
    			url: "/command",
    			data: JSON.stringify( command_dict ),
    			contentType: "application/json; charset=utf-8",
    			dataType: "json",
    			success: function(data){ getupdate(); console.log('success');},
    			failure: function(errMsg) {console.log('failed');}
			});
		}
	}
});
