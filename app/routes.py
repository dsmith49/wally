from app import app
from flask import render_template, request, jsonify
from os import getcwd, listdir

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/control')
def control():
	return render_template('control.html', title='Control')

@app.route('/settings')
def settings():
	return render_template('settings.html', title='Settings')

@app.route('/command', methods = ['POST'])
def command():
	content = request.json
	print(content['command'])
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
	path = getcwd()+"/images/"
	list_of_files = []
	for filename in listdir(path):
		if (filename.split('.')[1] == 'svg'):
			list_of_files.append( filename )
	return jsonify( list_of_files )

@app.route('/draw_svg', methods = ['GET','POST'])
def draw_svg():
	filename = request.json
	print('filename is', filename)
	return ('', 204)

