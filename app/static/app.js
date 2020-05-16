
var stats = document.createElement('div');
stats.id = 'stats_div';
var loc = document.createElement('p');
var node = document.createTextNode("motor:");
loc.appendChild(node);
stats.appendChild(loc);

//var canv = document.createElement('canvas');
//canv.id = 'someId';

document.body.appendChild(stats);
//document.body.appendChild(canv);

document.addEventListener('keydown', function(e) {
	if (document.activeElement === document.body ) {	
		var code = e.which || e.keyCode;
		if (([38,40,37,39]).includes(code)) { console.log('key pressed') }
		if (([32]).includes(code)) { console.log('key pressed') }
		if (([16]).includes(code)) { console.log('key pressed') }
		if (([18]).includes(code)) { console.log('key pressed') }
		if (([82]).includes(code)) { console.log('key pressed') }
		if (([27]).includes(code)) { console.log('key pressed') }
	}
});
