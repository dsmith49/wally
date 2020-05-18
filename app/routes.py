from app import app
from flask import render_template, request, jsonify
from os import getcwd, listdir
import threading

@app.route('/')
@app.route('/index')
def index():
	with open("README.md","r") as file:
		content = file.read()
		return render_template('index.html', title='Home', readme=content)

@app.route('/control')
def control():
	return render_template('control.html', title='Control')

@app.route('/settings')
def settings():
	return render_template('settings.html', title='Settings')

@app.route('/get_json_settings', methods = ['GET','POST'])
def settings_json():
	content = request.json
	print( content )
	if (content is None):
		print('in fetch settings')
		settings = app.config['wally'].settings()
		return settings
	else:
		print('in save settings')
		app.config['wally'].settings( settings = content )
		return ('', 204)
		

@app.route('/command', methods = ['POST'])
def command():
	content = request.json
	app.config['wally'].command( content )
	status = app.config['wally'].status()
	return jsonify( status )

@app.route('/status', methods = ['GET','POST'])
def status():
	status = app.config['wally'].status()
	print('in status and returning', status)
	return jsonify( status )

@app.route('/draw')
def draw():
	return render_template('draw.html', title='Settings')

@app.route('/svgfiles', methods = ['GET','POST'])
def svgfiles():
	path = getcwd()+"/app/static/images/"
	data = {}
	data['filenames'] = []
	data['progress'] = app.config['wally'].drawstatus
	for filename in listdir(path):
		if (filename.split('.')[1] == 'svg'):
			data['filenames'].append( filename )
	return jsonify( data )

@app.route('/draw_svg', methods = ['GET','POST'])
def draw_svg():
	filename = request.json
	print('filename is', filename)
	data = app.config['wally'].loadfile( getcwd() + '/app/static/images/' + filename )
	x = threading.Thread( target=app.config['wally'].drawSVG, args=(data,), daemon=True)
	x.start()
	#x.join()
	return ('', 204)

@app.route('/stop_draw_svg', methods = ['GET','POST'])
def stop_draw_svg():
	app.config['wally'].drawing = False
	return ('', 204)

