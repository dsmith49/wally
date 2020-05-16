from app import app
from flask import render_template, flash, redirect

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/command', methods = ['POST'])
def command(command_dict):
	print('command route says', command_dict)

