from app import app
from flask import render_template, request, jsonify

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/command', methods = ['POST'])
def command():
	content = request.json
	print(content['command'])
	app.config['wally'].command( content )
	status = app.config['wally'].status()
	return jsonify( status )
	#return ('', 204)

@app.route('/status', methods = ['GET','POST'])
def status():
	status = app.config['wally'].status()
	print('in status and returning', status)
	return jsonify( status )
