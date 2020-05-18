from app import app
from flask import render_template, request, jsonify
from os import getcwd, listdir, system
import threading

path = '/home/pi/wally/'
@app.route('/')
@app.route('/index')
def index():
	with open(path + "README.md","r") as file:
		content = file.read()
		return render_template('index.html', title='Home', readme=content)

@app.route('/control')
def control():
	return render_template('control.html', title='Control')

@app.route('/command', methods = ['POST'])
def command():
	content = request.json
	app.config['wally'].command( content )
	status = app.config['wally'].status()
	return jsonify( status )

@app.route('/status', methods = ['GET','POST'])
def status():
	status = app.config['wally'].status()
	return jsonify( status )

@app.route('/commandpi', methods = ['POST'])
def commandpi():
	content = request.json
	if (content['COMMAND'] == 'SHUTDOWN'):
		system('sudo shutdown -h now')
	if (content['COMMAND'] == 'REBOOT'):
		system('sudo shutdown -r now')
	return ('', 204)

@app.route('/settings')
def settings():
	return render_template('settings.html', title='Settings')

@app.route('/get_json_settings', methods = ['GET','POST'])
def settings_json():
	content = request.json
	print( content )
	if (content is None):
		settings = app.config['wally'].settings()
		return settings
	else:
		app.config['wally'].settings( settings = content )
		return ('', 204)

@app.route('/draw')
def draw():
	return render_template('draw.html', title='Settings')

@app.route('/svgfiles', methods = ['GET','POST'])
def svgfiles():
	svgpath = path+"/app/static/images/"
	data = {}
	data['filenames'] = []
	data['progress'] = app.config['wally'].drawstatus
	for filename in listdir(svgpath):
		if (filename.split('.')[1] == 'svg'):
			data['filenames'].append( filename )
	return jsonify( data )

@app.route('/draw_svg', methods = ['GET','POST'])
def draw_svg():
	filename = request.json
	data = app.config['wally'].loadfile( path + '/app/static/images/' + filename )
	x = threading.Thread( target=app.config['wally'].drawSVG, args=(data,), daemon=True)
	x.start()
	#x.join()
	return ('', 204)

@app.route('/stop_draw_svg', methods = ['GET','POST'])
def stop_draw_svg():
	app.config['wally'].drawing = False
	return ('', 204)

