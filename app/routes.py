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
	app.config['command'](content)
	return ('', 204)
